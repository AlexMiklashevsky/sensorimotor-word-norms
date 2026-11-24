# Maps a coded scale (category k, scale name) to a standard dimension label.
# Used by enrich_filters.py (which dimensions each paper rated) and plan_patch.py (examples per dimension).
# Category 3 labels carry a sense group: "visual: color", "touch/body: pain", "sound: loudness".
# Add rules here when new scale names appear; check_all.py lists unmapped scale names.
import re
R2=[('interoception',r'intero|inside (your|the) body|bodily sensation'),('vision',r'vis|see|sight|seeing|\bzien'),('hearing',r'hear|audit|acoust|sound|horen'),
    ('touch',r'touch|tactil|haptic|aanraking'),('taste',r'tast|gustat|proeven'),('smell',r'smell|olfact|ruiken')]
# 'action association' in category 5: only Paisios (2024), whose instruction asks how strongly the referent is "associated to a use with the hands"
# (decision 2026-11-24: belongs with manipulability). Action association without a body part is category 4.
R5=[('hand: graspability / manipulability (objects)',r'grasp|manipul|holdab|usab|manual action|action association'),('mouth/face',r'mouth|face|throat|articulat|tongue'),('head',r'^head|head \(|head without'),
    ('hand/arm: association',r'hand|arm|upperlimb|finger'),('foot/leg',r'foot|feet|leg|lowerlimb'),('torso',r'torso')]
R3=[('visual: color',r'colou?r'),('visual: shape/form',r'shape|form\b|visual form'),('visual: motion',r'motion|fast|slow'),('visual: brightness',r'bright|dark'),
    ('visual: size',r'large|small'),('visual: pattern/texture',r'pattern'),('visual: complexity',r'complex'),('visual: face/body',r'^face|^body'),
    ('several features (one question)',r'feeling types'),('touch/body: temperature',r'temperat|warm|cold'),('touch/body: texture',r'texture'),('touch/body: weight',r'weight'),('touch/body: pain',r'pain'),
    ('touch/body: balance',r'balance'),('touch/body: kinesthesis',r'kinesth'),('sound: loudness',r'loud'),('sound: pitch',r'^low|^high'),
    ('sound: music',r'music'),('sound: speech',r'speech'),('sound: sound',r'^sound')]
R4=[('relative embodiment',r'embodiment|body involvement'),('movement',r'^movement'),('motor content',r'motor content'),('effector involvement',r'effector'),
    ('action relatedness',r'action|motor|body-related|enactment')]
R1=[('global sensory experience (SER)',r'ser\b|sensory experience'),('bodily sensations',r'bodily sensation')]
R6=[('child BOI',r'child'),('BOI',r'^boi|body-object|potential physical|manipulation association'),('number of actions',r'number of actions'),
    ('manipulation',r'manipulat'),('practice / use',r'practice'),('action relatedness',r'action|motor')]
RULES={1:R1,2:R2,3:R3,4:R4,5:R5,6:R6}
MULTI={2:r'select|six perceptual|five senses|sense selection|feeling types',5:r'body part|body-part|arm/leg/face|foot/torso|body parts'}
def dim(k,scale):
    s=scale.lower().strip()
    if k in MULTI and re.search(MULTI[k],s): return 'several senses (one question)' if k==2 else 'which body part (one question)'
    for lab,rx in RULES[k]:
        if re.search(rx,s): return lab
    return 'other'
