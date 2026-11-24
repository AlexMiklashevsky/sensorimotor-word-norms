# Citation network analysis: citation counts, Louvain communities, stability, agreement with categories / language / study type.
# Input:  analysis/nodes.csv, analysis/edges.csv (written by export_for_r.py)
# Output: analysis/node_metrics.csv (per paper) and results.json (summary used by the web page)
# Run from the net/ folder:  Rscript analysis/communities.R
suppressMessages({library(igraph); library(jsonlite)})
invisible(suppressWarnings(Sys.setlocale("LC_CTYPE", "C.UTF-8")))  # paper labels contain non-ASCII letters
nodes <- read.csv("analysis/nodes.csv", fileEncoding = "UTF-8", stringsAsFactors = FALSE)
edges <- read.csv("analysis/edges.csv", fileEncoding = "UTF-8", stringsAsFactors = FALSE)
nodes$has_reference_list <- nodes$has_reference_list == 1
g <- graph_from_data_frame(edges, directed = TRUE, vertices = nodes)
yr <- setNames(nodes$year, nodes$id)

# citation counts; "potential citers" = later (or same-year) papers with a reference list, plus any actual citer
cited_by <- degree(g, mode = "in"); cites <- degree(g, mode = "out")
potential <- sapply(nodes$id, function(a) {
  later <- nodes$id[nodes$id != a & nodes$has_reference_list & nodes$year >= yr[a]]
  length(union(later, names(neighbors(g, a, mode = "in"))))
})
newer <- edges[yr[edges$cited] > yr[edges$citing], ]

# community detection: undirected graph without papers lacking a reference list and without isolates
to_undir <- if (exists("as_undirected")) as_undirected else as.undirected  # name differs between igraph versions
u <- to_undir(g, mode = "collapse")
u <- delete_vertices(u, nodes$id[!nodes$has_reference_list])
u <- delete_vertices(u, V(u)[degree(u) == 0])
ids <- sort(V(u)$name)
runs <- lapply(0:99, function(s) {
  set.seed(s); cl <- cluster_louvain(u, resolution = 1)
  m <- membership(cl)[ids]
  # relabel: largest community = 1; ties by alphabetically first member
  grp <- split(names(m), m)
  ord <- order(-lengths(grp), sapply(grp, min))
  lab <- setNames(integer(length(m)), names(m))
  for (i in seq_along(ord)) lab[grp[[ord[i]]]] <- i
  list(mod = modularity(cl), lab = lab)
})
mods <- sapply(runs, `[[`, "mod")
best <- runs[[which.max(mods)]]; com <- best$lab
# communities with fewer than MIN_SIZE papers are reported as "not assigned" (too small to interpret)
MIN_SIZE <- 3
small <- names(which(table(com) < MIN_SIZE))
unassigned <- names(com)[as.character(com) %in% small]
com <- com[!names(com) %in% unassigned]
com[] <- match(com, sort(unique(com)))  # renumber 1..k, order by size kept
ids <- names(com)
pairs <- combn(length(runs), 2)
stab <- apply(pairs, 2, function(p) compare(runs[[p[1]]]$lab, runs[[p[2]]]$lab, method = "adjusted.rand"))
cat_ <- nodes$main_category[match(ids, nodes$id)]; lan <- nodes$language[match(ids, nodes$id)]; sty <- nodes$study_type[match(ids, nodes$id)]
f <- function(x) as.integer(factor(x))
agree <- function(x, m) round(compare(f(x), com, method = m), 3)
# chance level of the category agreement: shuffle the category labels 2,000 times
set.seed(2026)
null_nmi <- replicate(2000, compare(sample(f(cat_)), com, method = "nmi"))

# composition of each community
comp <- list()
for (k in sort(unique(com))) {
  mem <- names(com)[com == k]
  co <- if (length(mem) > 1) apply(combn(mem, 2), 2, function(p) mean(sapply(runs, function(r) r$lab[p[1]] == r$lab[p[2]]))) else 1
  tab <- function(x, n = 99) { t <- sort(table(x), decreasing = TRUE); t <- head(t, n); lapply(names(t), function(nm) list(nm, as.integer(t[[nm]]))) }
  top <- head(mem[order(-cited_by[mem], mem)], 8)
  comp[[as.character(k)]] <- list(size = length(mem),
    categories = tab(nodes$main_category[match(mem, nodes$id)]), languages = tab(nodes$language[match(mem, nodes$id)], 6),
    top = lapply(top, function(v) list(v, unname(cited_by[v]))), mean_coassign = round(mean(co), 3), min_coassign = round(min(co), 3),
    together_all = sum(sapply(runs, function(r) length(unique(r$lab[mem])) == 1)), study = tab(nodes$study_type[match(mem, nodes$id)]))
}
mix <- function(a, b) { t <- table(paste0(a, b)); setNames(as.list(as.integer(t)), names(t)) }
mc <- nodes$main_category; names(mc) <- nodes$id
st <- nodes$study_type; names(st) <- nodes$id
topc <- head(nodes$id[order(-cited_by, nodes$id)], 12)
res <- list(
  n_nodes_graph = vcount(g), n_edges = ecount(g), n_edges_graph = ecount(g), n_nodes_community = vcount(u), n_edges_community = ecount(u),
  modularity_best = round(max(mods), 3), modularity_range = round(range(mods), 3), n_communities = length(unique(com)),
  stability_mean_ARI = round(mean(stab), 3), stability_min_ARI = round(min(stab), 3),
  ARI_vs_cluster = agree(cat_, "adjusted.rand"), NMI_vs_cluster = agree(cat_, "nmi"),
  ARI_vs_language = agree(lan, "adjusted.rand"), NMI_vs_language = agree(lan, "nmi"),
  ARI_vs_study = agree(sty, "adjusted.rand"), NMI_vs_study = agree(sty, "nmi"),
  NMI_vs_cluster_null_mean = round(mean(null_nmi), 3), NMI_vs_cluster_null_p99 = round(quantile(null_nmi, 0.99)[[1]], 3), NMI_vs_cluster_null_max = round(max(null_nmi), 3),
  newer_cited_edges = nrow(newer), newer_examples = lapply(seq_len(min(8, nrow(newer))), function(i) c(newer$citing[i], newer$cited[i])),
  min_community_size = MIN_SIZE, unassigned = unassigned, n_unassigned = length(unassigned),
  isolates = setdiff(nodes$id[nodes$has_reference_list], V(u)$name), hollow = nodes$id[!nodes$has_reference_list],
  communities = comp, top_cited = lapply(topc, function(v) list(v, unname(cited_by[v]), unname(potential[v]))),
  edges_same_category = round(mean(mc[edges$citing] == mc[edges$cited]), 3),
  category_mixing = { t <- table(paste0(substr(mc[edges$citing], 1, 1), "->", substr(mc[edges$cited], 1, 1))); setNames(as.list(as.integer(t)), names(t)) },
  studytype_mixing = { t <- sort(table(paste(st[edges$citing], "->", st[edges$cited])), decreasing = TRUE); setNames(as.list(as.integer(t)), names(t)) },
  software = paste0(R.version.string, "; igraph ", packageVersion("igraph"), "; jsonlite ", packageVersion("jsonlite")))
write_json(res, "results.json", auto_unbox = TRUE, pretty = TRUE, digits = NA)
write.csv(data.frame(id = nodes$id, cited_by = unname(cited_by[nodes$id]), cites = unname(cites[nodes$id]), potential_citers = unname(potential[nodes$id]),
                     community = unname(com[nodes$id])), "analysis/node_metrics.csv", row.names = FALSE, na = "", fileEncoding = "UTF-8")
cat("R analysis done:", vcount(u), "papers in", length(unique(com)), "communities; modularity", round(max(mods), 3),
    "; NMI with main category", agree(cat_, "nmi"), "(chance mean", round(mean(null_nmi), 3), ")\n")
