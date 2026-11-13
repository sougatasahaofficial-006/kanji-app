import os
import json
import xml.etree.ElementTree as ET

KANJIVG_DIR = "kanjivg-data"
PART2_JSON_PATH = "n1_part2.json"
PART3_JSON_PATH = "n1_part3.json"

N1_PART3_DATA = [
    # Lesson 251
    [
        ("拭く", "ふく", "to wipe / dry", ["ショク"], ["ふ.く", "ぬぐ.う"]),
        ("口が堅い", "くちがかたい", "close-mouthed / tight-lipped / discreet", [], ["くちがかた.い"]),
        ("壇", "だん", "podium / stage / rostrum / terrace", ["ダン", "タン"], []),
        ("花壇", "かだん", "flower bed", ["カダン"], []),
        ("堅", "けん", "strict / hard / solid / tough / tight / reliable", ["ケン"], ["かた.い"]),
    ],
    # Lesson 252
    [
        ("呉れる", "くれる", "to give / let one have / do for one", ["ゴ"], ["く.れる"]),
        ("呉れ呉れも", "くれぐれも", "repeatedly / sincerely / earnestly", ["ゴ"], ["くれぐれも"]),
        ("暇", "ひま", "spare time / free time / leisure", ["カ"], ["ひま", "いとま"]),
        ("休暇", "きゅうか", "holiday / day off / furlough / absence (from work)", ["キュウカ"], []),
        ("零す", "こぼす", "to spill / drop / shed (tears) / grumble", ["レイ"], ["こぼ.す"]),
    ],
    # Lesson 253
    [
        ("塞ぐ", "ふさぐ", "to stop up / close up / block (up) / plug up / shut up", ["ソク", "サイ"], ["ふさ.ぐ", "ふさ.がる"]),
        ("塞がる", "ふさがる", "to be plugged up / be shut up / be closed / be occupied", ["ソク", "サイ"], ["ふさ.がる"]),
        ("岳", "たけ", "point / peak / mountain", ["ガク"], ["たけ"]),
        ("山岳", "さんがく", "mountains", ["サンガク"], []),
        ("空襲", "くうしゅう", "air raid / air attack", ["クウシュウ"], []),
    ],
    # Lesson 254
    [
        ("蹴る", "ける", "to kick / refuse / reject", ["シュウ"], ["け.る"]),
        ("鍵", "かぎ", "key / lock", ["ケン"], ["かぎ"]),
        ("臓", "ぞう", "entrails / viscera / bowels", ["ゾウ"], ["はらわた"]),
        ("罰", "ばつ", "penalty / punishment", ["バツ", "バチ", "ハツ"], ["ばっ.する"]),
        ("稼働", "かどう", "operation (of machine) / running / working", ["カドウ"], []),
    ],
    # Lesson 255
    [
        ("罰する", "ばっする", "to punish / penalize", ["バツ"], ["ばっ.する"]),
        ("刑罰", "けいばつ", "judgment / penalty / punishment", ["ケイバツ"], []),
        ("処罰", "しょばつ", "punishment", ["ショバツ"], []),
        ("漏る", "もる", "to leak / run out", ["ロウ"], ["も.る", "も.れる"]),
        ("愛想", "あいそ", "amiability / friendliness / hospitality / bill", ["アイソ"], []),
    ],
    # Lesson 256
    [
        ("漏れる", "もれる", "to leak out / escape / come through / shine through", ["ロウ"], ["も.れる"]),
        ("漏らす", "もらす", "to let leak / reveal / divulge / omit / wet one's pants", ["ロウ"], ["も.らす"]),
        ("ご覧になる", "ごらんになる", "to see / look / watch (honorific)", ["ゴラン"], []),
        ("回覧", "かいらん", "circulation / reading and passing round", ["カイラン"], []),
        ("君主", "くんしゅ", "ruler / monarch / sovereign", ["クンシュ"], []),
    ],
    # Lesson 257
    [
        ("観覧", "かんらん", "viewing / inspection", ["カンラン"], []),
        ("御覧", "ごらん", "seeing / looking / watching (honorific)", ["ゴラン"], []),
        ("御覧なさい", "ごらんなさい", "(please) look / (please) try to do", ["ゴラン"], []),
        ("展覧会", "てんらんかい", "exhibition", ["テンランカイ"], []),
        ("嫌悪", "けんお", "disgust / hate / repugnance / loathing", ["ケンオ"], []),
    ],
    # Lesson 258
    [
        ("漂う", "ただよう", "to drift / float / waft (e.g. scent) / hang in the air", ["ヒョウ"], ["ただよ.う"]),
        ("寂しい", "さびしい", "lonely / lonesome / solitary / desolate", ["セキ", "ジャク"], ["さび.しい", "さみ.しい"]),
        ("嘆く", "なげく", "to sigh / lament / grieve / mourn / deplore", ["タン"], ["なげ.く"]),
        ("禅", "ぜん", "Zen (Buddhism) / silent meditation", ["ゼン", "セン"], ["しずか", "ゆず.る"]),
        ("吉田", "よしだ", "Yoshida (surname)", [], ["よしだ"]),
    ],
    # Lesson 259
    [
        ("酷い", "ひどい", "cruel / heartless / hard / harsh / severe / violent", ["コク"], ["ひど.い"]),
        ("刃", "は", "edge (of a knife or sword) / blade", ["ジン", "ニン"], ["は", "やいば"]),
        ("漫", "まん", "cartoon / involuntarily / unrestrained / in spite of oneself", ["マン"], []),
        ("漫画", "まんが", "cartoon / comic / comic strip / manga", ["マンガ"], []),
        ("土砂", "どしゃ", "earth and sand / sediment", ["ドシャ"], []),
    ],
    # Lesson 260
    [
        ("矛", "ほこ", "halberd / arms / festival float", ["ム", "ボウ"], ["ほこ"]),
        ("霧", "きり", "fog / mist", ["ム", "ボウ", "ブ"], ["きり"]),
        ("暑い", "あつい", "hot (weather, etc.) / warm", ["ショ"], ["あつ.い"]),
        ("蒸し暑い", "むしあつい", "humid / sultry", [], ["むしあつ.い"]),
        ("虚偽", "きょぎ", "falsehood / untruth / lie / misinformation", ["キョギ"], []),
    ],
    # Lesson 261
    [
        ("猛暑日", "もうしょび", "extremely hot day (35°C or above)", ["モウショビ"], []),
        ("棚", "たな", "shelf / ledge / rack / trellis", ["ホウ"], ["たな"]),
        ("戸棚", "とだな", "cupboard / locker / closet / wardrobe", [], ["とだな"]),
        ("本棚", "ほんだな", "bookshelves / bookshelf / bookcase", [], ["ほんだな"]),
        ("猛", "もう", "fierce / rave / rush / become furious / wildness / strength", ["モウ"], []),
    ],
    # Lesson 262
    [
        ("袖", "そで", "sleeve / wing (of a stage, desk, gate)", ["シュウ"], ["そで"]),
        ("半袖", "はんそで", "short sleeves", [], ["はんそで"]),
        ("壮", "そう", "robust / manhood / prosperity", ["ソウ"], ["さかん"]),
        ("壮大", "そうだい", "magnificent / grand / majestic / splendid", ["ソウダイ"], []),
        ("供養", "くよう", "memorial service / Buddhist mass for the dead", ["クヨウ"], []),
    ],
    # Lesson 263
    [
        ("旬", "しゅん", "season (for specific products) / 10-day period", ["ジュン", "シュン"], []),
        ("上旬", "じょうじゅん", "first ten days of a month", ["ジョウジュン"], []),
        ("中旬", "ちゅうじゅん", "second third of a month / from the 11th to the 20th day", ["チュウジュン"], []),
        ("下旬", "げじゅん", "last ten days of a month", ["ゲジュン"], []),
        ("突如", "とつじょ", "suddenly / all of a sudden", ["トツジョ"], []),
    ],
    # Lesson 264
    [
        ("彫る", "ほる", "to carve / engrave / sculpt / chisel", ["チョウ"], ["ほ.る"]),
        ("彫刻", "ちょうこく", "carving / engraving / sculpture", ["チョウコク"], []),
        ("鎖", "くさり", "chain / chains / connection", ["サ"], ["くさり", "とざ.す"]),
        ("閉鎖", "へいさ", "closing / closure / shutdown / lockout", ["ヘイサ"], []),
        ("神宮", "じんぐう", "Shinto shrine (esp. Ise Jingu)", ["ジングウ"], []),
    ],
    # Lesson 265
    [
        ("封鎖", "ふうさ", "blockade / freezing (funds)", ["フウサ"], []),
        ("潰す", "つぶす", "to smash / crush / flatten / shut down / waste (time)", ["カイ"], ["つぶ.す", "つぶ.れる"]),
        ("縦", "たて", "the vertical / height / front-to-back / length", ["ジュウ"], ["たて"]),
        ("縦書き", "たてがき", "vertical writing", [], ["たてがき"]),
        ("操縦", "そうじゅう", "steering / piloting / flying / control / manipulation", ["ソウジュウ"], []),
    ],
    # Lesson 266
    [
        ("粧", "しょう", "cosmetics / adorn (one's person)", ["ショウ"], []),
        ("化粧", "けしょう", "make-up / makeup / cosmetics", ["ケショウ"], []),
        ("化粧品", "けしょうひん", "cosmetics / toiletries", ["ケショウヒン"], []),
        ("慌てる", "あわてる", "to become confused (disconcerted, disorganized) / be flustered / panic", ["コウ"], ["あわ.てる", "あわ.ただしい"]),
        ("和らげる", "やわらげる", "to soften / calm down / pacify / ease / alleviate / mitigate", ["ワ"], ["やわ.らげる"]),
    ],
    # Lesson 267
    [
        ("慌ただしい", "あわただしい", "busy / hurried / confused / flurried", ["コウ"], ["あわ.ただしい"]),
        ("穏やか", "おだやか", "calm / gentle / quiet / peaceful / moderate", ["オン"], ["おだ.やか"]),
        ("枠", "わく", "frame / framework / spindle / spool / bounding box", [], ["わく"]),
        ("謎", "なぞ", "riddle / puzzle / enigma / mystery", ["メイ", "ベイ"], ["なぞ"]),
        ("枠組み", "わくぐみ", "frame / framework / outline", [], ["わくぐみ"]),
    ],
    # Lesson 268
    [
        ("謎謎", "なぞなぞ", "riddle / puzzle / enigma", [], ["なぞなぞ"]),
        ("誉", "ほまれ", "reputation / praise / honor / glory", ["ヨ"], ["ほま.れ", "ほ.める"]),
        ("名誉", "めいよ", "honor / honour / credit / prestige", ["メイヨ"], []),
        ("逸れる", "それる", "to turn away / bear off / veer away / stray from / miss", ["イツ"], ["そ.れる", "そ.らす"]),
        ("城下", "じょうか", "land near a castle / castle town", ["ジョウカ"], []),
    ],
    # Lesson 269
    [
        ("逸らす", "そらす", "to turn away (e.g. one's eyes) / divert / avert / dodge", ["イツ"], ["そ.らす"]),
        ("惜しい", "おしい", "regrettable / disappointing / precious / dear / almost", ["セキ"], ["お.しい", "お.しむ"]),
        ("措", "そ", "set aside / give up / suspend / discontinue / lay aside / except", ["ソ"], ["お.く"]),
        ("琴", "こと", "koto (13-stringed Japanese zither)", ["キン"], ["こと"]),
        ("措置", "そち", "measure / step / action", ["ソチ"], []),
    ],
    # Lesson 270
    [
        ("拍", "はく", "clap / beat (music)", ["ハク", "ヒョウ"], []),
        ("拍手", "はくしゅ", "clapping hands / applause", ["ハクシュ"], []),
        ("稽古", "けいこ", "practice / training / study", ["ケイコ"], []),
        ("礎", "いしずえ", "foundation stone / cornerstone / basis", ["ソ"], ["いしずえ"]),
        ("稽", "けい", "think / consider / bicker / bow", ["ケイ"], ["かんが.える"]),
    ],
    # Lesson 271
    [
        ("基礎", "きそ", "foundation / basis", ["キソ"], []),
        ("遭う", "あう", "to meet / encounter (undesirable nuance)", ["ソウ"], ["あ.う"]),
        ("掌", "てのひら", "palm of the hand", ["ショウ"], ["てのひら", "たなごころ"]),
        ("車掌", "しゃしょう", "(train) conductor", ["シャショウ"], []),
        ("拍子", "ひょうし", "time / tempo / beat / rhythm / the moment", ["ヒョウシ"], []),
    ],
    # Lesson 272
    [
        ("鍋", "なべ", "saucepan / pot / stew / hot pot", ["カ"], ["なべ"]),
        ("据える", "すえる", "to set (table) / lay (foundation) / place (gun) / apply (moxa)", ["キョ"], ["す.える", "す.わる"]),
        ("跳ぶ", "とぶ", "to jump / leap / spring / bound / hop", ["チョウ"], ["と.ぶ", "は.ねる"]),
        ("跳ねる", "はねる", "to jump / leap / prance / spring up / spatter / splash", ["チョウ"], ["は.ねる", "と.ぶ"]),
        ("遭遇", "そうぐう", "encounter", ["ソウグウ"], []),
    ],
    # Lesson 273
    [
        ("縛る", "しばる", "to tie / bind / fasten / restrict", ["バク"], ["しば.る"]),
        ("束縛", "そくばく", "restraint / restriction / fetters / yoke / shackles", ["ソクバク"], []),
        ("雷", "かみなり", "lightning / thunder / thunderbolt", ["ライ"], ["かみなり", "いかずち"]),
        ("恨み", "うらみ", "resentment / grudge / malice / bitterness", ["コン"], ["うら.み"]),
        ("炎症", "えんしょう", "inflammation / irritation", ["エンショウ"], []),
    ],
    # Lesson 274
    [
        ("恨む", "うらむ", "to bear a grudge against / resent / blame / curse", ["コン"], ["うら.む", "うら.めしい"]),
        ("顕", "けん", "appear / existing", ["ケン"], ["あきらか", "あらわ.れる"]),
        ("顕微鏡", "けんびきょう", "microscope", ["ケンビキョウ"], []),
        ("殖える", "ふえる", "to increase / multiply", ["ショク"], ["ふ.える", "ふ.やす"]),
        ("残酷", "ざんこく", "cruelty / mercilessness / ruthlessness / brutality", ["ザンコク"], []),
    ],
    # Lesson 275
    [
        ("殖やす", "ふやす", "to increase / add to / augment", ["ショク"], ["ふ.やす"]),
        ("繁殖", "はんしょく", "breed / multiply / increase / propagation", ["ハンショク"], []),
        ("寧ろ", "むしろ", "rather / better / instead", ["ネイ"], ["むし.ろ"]),
        ("丁寧", "ていねい", "polite / courteous / civil / careful / close / thorough", ["テイネイ"], []),
        ("高揚", "こうよう", "enhancement / exaltation / promotion / uplift", ["コウヨウ"], []),
    ],
    # Lesson 276
    [
        ("湧く", "わく", "to well (up) / gush forth (of water) / spring out / surge", ["ユウ"], ["わ.く"]),
        ("巧み", "たくみ", "skill / cleverness / deftness / ingenuity", ["コウ"], ["たく.み", "たく.む"]),
        ("巧妙", "こうみょう", "ingenious / skillful / clever / deft", ["コウミョウ"], []),
        ("精巧", "せいこう", "elaborate / delicate / exquisite", ["セイコウ"], []),
        ("過ち", "あやまち", "fault / error / indiscretion / faux pas", ["カ"], ["あやま.ち"]),
    ],
    # Lesson 277
    [
        ("浸す", "ひたす", "to soak / dip / steep / immerse / moisten / wet", ["シン"], ["ひた.す", "ひた.る"]),
        ("浸ける", "つける", "to dip in / soak / pickle", ["シン"], ["つ.ける"]),
        ("隔てる", "へだてる", "to separate (by distance, time, etc.) / isolate / partition", ["カク"], ["へだ.てる"]),
        ("隔たる", "へだたる", "to be distant / be separated", ["カク"], ["へだ.たる"]),
        ("浸透", "しんとう", "permeation / infiltration / osmosis / spread (of thought, etc.)", ["シントウ"], []),
    ],
    # Lesson 278
    [
        ("間隔", "かんかく", "space / interval / SPC", ["カンカク"], []),
        ("隔週", "かくしゅう", "every other week / biweekly", ["カクシュウ"], []),
        ("班", "はん", "squad / corps / unit / group", ["ハン"], []),
        ("甚だ", "はなはだ", "very / greatly / exceedingly", ["ジン"], ["はなは.だ"]),
        ("風潮", "ふうちょう", "tendency / trend / tide / current", ["フウチョウ"], []),
    ],
    # Lesson 279
    [
        ("甚だしい", "はなはだしい", "extreme / excessive / terrible / intense / severe", ["ジン"], ["はなは.だしい"]),
        ("獣", "けもの", "beast / brute / animal", ["ジュウ"], ["けもの", "けだもの"]),
        ("怪獣", "かいじゅう", "monster", ["カイジュウ"], []),
        ("疾", "しつ", "rapidly", ["シツ"], ["はや.い"]),
        ("疾患", "しっかん", "disease / ailment / illness", ["シッカン"], []),
    ],
    # Lesson 280
    [
        ("塾", "じゅく", "cram school / private tutoring school", ["ジュク"], []),
        ("相撲", "すもう", "sumo wrestling / wrestler", ["スモウ"], []),
        ("塊", "かたまり", "lump / mass / bundle / clump / clod / cluster", ["カイ", "ケ"], ["かたまり", "つちくれ"]),
        ("絞る", "しぼる", "to press / wring / squeeze", ["コウ"], ["しぼ.る", "し.める"]),
        ("撲", "ぼく", "slap / strike / hit / beat / tell / speak", ["ボク"], []),
    ],
    # Lesson 281
    [
        ("履く", "はく", "to put on (lower-body clothing, e.g. pants, skirt, footwear)", ["リ"], ["は.く"]),
        ("履歴書", "りれきしょ", "personal history / curriculum vitae / resume", ["リレキショ"], []),
        ("苗", "なえ", "seedling / sapling / shoot", ["ビョウ", "ミョウ"], ["なえ", "なわ-"]),
        ("冗", "じょう", "superfluous / uselessness", ["ジョウ"], []),
        ("疾病", "しっぺい", "illness / disease", ["シッペイ"], []),
    ],
    # Lesson 282
    [
        ("冗談", "じょうだん", "jest / joke / funny story", ["ジョウダン"], []),
        ("陶", "とう", "pottery / porcelain", ["トウ"], []),
        ("陶器", "とうき", "pottery / ceramics", ["トウキ"], []),
        ("励む", "はげむ", "to work hard / try hard / strive / endeavor", ["レイ"], ["はげ.む", "はげ.ます"]),
        ("熱湯", "ねっとう", "boiling water", ["ネットウ"], []),
    ],
    # Lesson 283
    [
        ("励ます", "はげます", "to encourage / cheer / raise (the voice)", ["レイ"], ["はげ.ます"]),
        ("激励", "げきれい", "encouragement / urging / incitement / inspiration", ["ゲキレイ"], []),
        ("陳", "ちん", "exhibit / state / relate / explain", ["チン"], ["ひ.ねる"]),
        ("陳列", "ちんれつ", "exhibition / display / put on show", ["チンレツ"], []),
        ("右翼", "うよく", "right-wing / right flank", ["ウヨク"], []),
    ],
    # Lesson 284
    [
        ("猿", "さる", "monkey (esp. the Japanese macaque) / ape / non-human primate", ["エン"], ["さる"]),
        ("傘", "かさ", "umbrella / parasol", ["サン"], ["かさ"]),
        ("啓", "けい", "disclose / open / say", ["ケイ"], ["ひら.く", "さと.す"]),
        ("拝啓", "はいけい", "Dear (Sir/Madam)", ["ハイケイ"], []),
        ("下駄", "げた", "geta (Japanese wooden clogs)", ["ゲタ"], []),
    ],
    # Lesson 285
    [
        ("劣る", "おとる", "to be inferior to / be less good at / fall behind", ["レツ"], ["おと.る"]),
        ("殴る", "なぐる", "to strike / beat / hit", ["オウ"], ["なぐ.る"]),
        ("盾", "たて", "shield / buckler / escutcheon / pretext", ["ジュン"], ["たて"]),
        ("衰える", "おとろえる", "to become weak / decline / wear / abate / decay / wither", ["スイ"], ["おとろ.える"]),
        ("矛盾", "むじゅん", "contradiction / inconsistency", ["ムジュン"], []),
    ],
    # Lesson 286
    [
        ("老衰", "ろうすい", "senility / senile decay", ["ロウスイ"], []),
        ("滝", "たき", "waterfall", ["ロウ", "ソウ"], ["たき"]),
        ("慰める", "なぐさめる", "to comfort / console / amuse", ["イ"], ["なぐさ.める", "なぐさ.む"]),
        ("蛇", "へび", "snake / serpent", ["ジャ", "ダ", "イ"], ["へび"]),
        ("縄文", "じょうもん", "straw-rope pattern / Jomon (period)", ["ジョウモン"], []),
    ],
    # Lesson 287
    [
        ("蛇口", "じゃぐち", "faucet / tap", ["ジャグチ"], []),
        ("癖", "くせ", "habit (often a bad habit) / peculiarity / idiosyncrasy", ["ヘキ"], ["くせ", "くせ.に"]),
        ("潤う", "うるおう", "to be moist / be damp / get wet / profit by / be enriched", ["ジュン"], ["うるお.う", "うるお.す"]),
        ("利潤", "りじゅん", "profit / returns", ["リジュン"], []),
        ("井上", "いのうえ", "Inoue (surname)", [], ["いのうえ"]),
    ],
    # Lesson 288
    [
        ("鉢", "はち", "bowl / pot / basin / flowerpot / crown / brainpan", ["ハチ", "ハツ"], []),
        ("戯れ", "たわむれ", "play / sport / joke / flirtation", ["ギ", "ゲ"], ["たわむ.れ"]),
        ("悪戯", "いたずら", "teasing / prank / trick / practical joke / mischief", ["アクギ"], ["いたずら"]),
        ("罷", "ひ", "quit / stop / leave / withdraw / go", ["ヒ"], ["まか.り-", "や.める"]),
        ("同伴", "どうはん", "accompanying / going with", ["ドウハン"], []),
    ],
    # Lesson 289
    [
        ("偏", "へん", "partial / side / left-side radical of a character / inclining", ["ヘン"], ["かたよ.る"]),
        ("偏る", "かたよる", "to lean (to one side) / incline / be biased / be partial", ["ヘン"], ["かたよ.る"]),
        ("巣", "す", "nest / rookery / breeding place / beehive / cobweb / den", ["ソウ"], ["す", "す.くう"]),
        ("宴", "うたげ", "banquet / feast / party", ["エン"], ["うたげ"]),
        ("書斎", "しょさい", "study / library / den / home office", ["ショサイ"], []),
    ],
    # Lesson 290
    [
        ("宴会", "えんかい", "party / banquet / reception / feast / dinner", ["エンカイ"], []),
        ("棟", "むね", "ridgepole / ridge / counter for buildings", ["トウ"], ["むね", "むな-"]),
        ("潔い", "いさぎよい", "manly / sportsmanlike / pure / upright / graceful", ["ケツ"], ["いさぎよ.い"]),
        ("清潔", "せいけつ", "clean / hygienic / sanitary", ["セイケツ"], []),
        ("鹿児島", "かごしま", "Kagoshima", [], ["かごしま"]),
    ],
    # Lesson 291
    [
        ("不潔", "ふけつ", "unclean / dirty / filthy / impure", ["フケツ"], []),
        ("膜", "まく", "membrane", ["マク"], []),
        ("乏しい", "とぼしい", "meagre / meager / scarce / limited / destitute / poor", ["ボウ"], ["とぼ.しい", "とも.しい"]),
        ("貧乏", "びんぼう", "poverty-stricken / destitute / poor / penurious", ["ビンボウ"], []),
        ("封建", "ほうけん", "feudalistic", ["ホウケン"], []),
    ],
    # Lesson 292
    [
        ("舗", "ほ", "shop / store / pave", ["ホ"], []),
        ("舗装", "ほそう", "pavement / road surface", ["ホソウ"], []),
        ("睡眠", "すいみん", "sleep", ["スイミン"], []),
        ("睡眠不足", "すいみんぶそく", "lack of sleep / sleep deprivation", ["スイミンブソク"], []),
        ("睡", "すい", "drowsy / sleep / die", ["スイ"], ["ねむ.る"]),
    ],
    # Lesson 293
    [
        ("睡眠時間", "すいみんじかん", "hours of sleep / sleeping time", ["スイミンジカン"], []),
        ("賭け", "かけ", "bet / wager / gamble", ["ト"], ["か.け"]),
        ("賭ける", "かける", "to wager / bet / risk / stake / gamble", ["ト"], ["か.ける"]),
        ("括る", "くくる", "to tie up / tie together / bind / bundle / hang", ["カツ"], ["くく.る"]),
        ("店舗", "てんぽ", "shop / store", ["テンポ"], []),
    ],
    # Lesson 294
    [
        ("一括", "いっかつ", "lumping together / summing up / bundle / lump", ["イッカツ"], []),
        ("貢", "みつぎ", "tribute / support / finance", ["コウ", "ク"], ["みつ.ぐ"]),
        ("貢献", "こうけん", "contribution (furthering a goal or cause) / services", ["コウケン"], []),
        ("卑しい", "いやしい", "lowly / humble / vulgar / coarse / greedy / mean", ["ヒ"], ["いや.しい", "いや.しむ"]),
        ("着工", "ちゃっこう", "starting (construction) work", ["チャッコウ"], []),
    ],
    # Lesson 295
    [
        ("貼る", "はる", "to stick / paste / affix", ["テン", "チョウ"], ["は.る", "つ.く"]),
        ("挿す", "さす", "to insert / put in / graft / wear in belt", ["ソウ"], ["さ.す", "はさ.む"]),
        ("挿入", "そうにゅう", "insertion / incorporation / infixing", ["ソウニュウ"], []),
        ("翻す", "ひるがえす", "to turn over / wave / flutter / change (one's mind)", ["ホン", "ハン"], ["ひるがえ.す"]),
        ("川原", "かわら", "dry riverbed / river beach", [], ["かわら"]),
    ],
    # Lesson 296
    [
        ("翻訳", "ほんやく", "translation", ["ホンヤク"], []),
        ("枕", "まくら", "pillow / bolster", ["チン", "シン"], ["まくら"]),
        ("錯イオン", "さくイオン", "complex ion", ["サク"], []),
        ("錯覚", "さっかく", "optical illusion / hallucination / misapprehension / delusion", ["サッカク"], []),
        ("離脱", "りだつ", "withdrawal / secession / separation / breakaway", ["リダツ"], []),
    ],
    # Lesson 297
    [
        ("錯誤", "さくご", "mistake / error / discrepancy", ["サクゴ"], []),
        ("謙る", "へりくだる", "to deprecate oneself and praise the listener / abase oneself", ["ケン"], ["へりくだ.る"]),
        ("蓄える", "たくわえる", "to store / lay in stock / save / keep / wear (a beard)", ["チク"], ["たくわ.える"]),
        ("蓄積", "ちくせき", "accumulation / accumulate / store", ["チクセキ"], []),
        ("紫外線", "しがいせん", "ultraviolet rays / UV radiation", ["シガイセン"], []),
    ],
    # Lesson 298
    [
        ("貯蓄", "ちょちく", "savings", ["チョチク"], []),
        ("拓く", "ひらく", "to break up (new land) / open up / clear", ["タク"], ["ひら.く"]),
        ("開拓", "かいたく", "reclamation (e.g. wasteland) / cultivation / pioneering", ["カイタク"], []),
        ("鼓", "つづみ", "drum / beat / rouse / muster", ["コ"], ["つづみ"]),
        ("執着", "しゅうちゃく", "attachment / adhesion / tenacity / fixation", ["シュウチャク"], []),
    ],
    # Lesson 299
    [
        ("太鼓", "たいこ", "drum / tambourine", ["タイコ"], []),
        ("粋", "いき", "chic / style / purity / essence", ["スイ"], ["いき"]),
        ("純粋", "じゅんすい", "pure / true / genuine / unmixed", ["ジュンスイ"], []),
        ("尉", "い", "military officer / jailer / old man / rank", ["イ", "ジョウ"], []),
        ("大尉", "たいい", "captain (Army, Air Force) / lieutenant (Navy)", ["タイイ"], []),
    ],
    # Lesson 300
    [
        ("粘る", "ねばる", "to be sticky / be adhesive / persevere / persist / stick to", ["ネン"], ["ねば.る"]),
        ("粘り", "ねばり", "stickiness / viscosity / tenacity / persistence", ["ネン"], ["ねば.り"]),
        ("徐行", "じょこう", "going slowly / proceeding at a crawl", ["ジョコウ"], []),
        ("堪える", "たえる", "to bear / stand / endure / put up with", ["カン", "タン"], ["た.える", "たま.る"]),
        ("徐", "じょ", "gradually / slowly / deliberately / gently", ["ジョ"], ["おもむろ.に"]),
    ],
    # Lesson 301
    [
        ("堪える", "こらえる", "to bear / stand / endure / put up with / restrain", ["カン", "タン"], ["こら.える", "た.える"]),
        ("堪える", "こたえる", "to have an intense effect on / take a toll on / feel keenly", ["カン", "タン"], ["こた.える"]),
        ("堪らない", "たまらない", "intolerable / unbearable / unendurable / irresistible", ["カン", "タン"], ["たま.らない"]),
        ("冠", "かんむり", "crown / diadem / first / best / peerless / cap", ["カン"], ["かんむり"]),
        ("粘土", "ねんど", "clay", ["ネンド"], []),
    ],
    # Lesson 302
    [
        ("冠", "かん", "crown / cap", ["カン"], ["かんむり"]),
        ("愉快", "ゆかい", "pleasant / delightful / enjoyable / joyful / cheerful", ["ユカイ"], []),
        ("尿", "にょう", "urine", ["ニョウ"], ["ゆばり", "いばり"]),
        ("顎", "あご", "jaw / chin", ["ガク"], ["あご", "えら"]),
        ("愉", "ゆ", "pleasure / happy / rejoice", ["ユ"], ["たの.しい", "たの.しむ"]),
    ],
    # Lesson 303
    [
        ("誓う", "ちかう", "to swear / vow / take an oath / pledge", ["セイ"], ["ちか.う"]),
        ("憂い", "うれい", "grief / sorrow / distress / anxiety / fear", ["ユウ"], ["うれ.い", "うれ.える"]),
        ("糧", "かて", "food / provisions / nourishment / sustenance", ["リョウ", "ロウ"], ["かて"]),
        ("食糧", "しょくりょう", "food (esp. staple food such as rice or wheat) / provisions", ["ショクリョウ"], []),
        ("滑走", "かっそう", "gliding / coasting / sliding / taxiing (of an airplane)", ["カッソウ"], []),
    ],
    # Lesson 304
    [
        ("架", "か", "erect / frame / mount / support / shelf / construct", ["カ"], ["か.ける", "か.かる"]),
        ("担架", "たんか", "stretcher / litter", ["タンカ"], []),
        ("架空", "かくう", "aerial / overhead / fictitious / imaginary / fabricated", ["カクウ"], []),
        ("芽", "め", "sprout / shoot / bud", ["ガ"], ["め"]),
        ("国旗", "こっき", "national flag", ["コッキ"], []),
    ],
    # Lesson 305
    [
        ("発芽", "はつが", "germination / sprouting / budding", ["ハツガ"], []),
        ("軸", "じく", "axis / shaft / axle / center / focal point / scroll", ["ジク"], []),
        ("苛める", "いじめる", "to ill-treat / bully / torment / persecute / tease", ["カ"], ["いじ.める"]),
        ("蓋", "ふた", "cover / lid / cap", ["ガイ", "カイ", "コウ"], ["ふた"]),
        ("石垣", "いしがき", "stone wall", [], ["いしがき"]),
    ],
    # Lesson 306
    [
        ("蓋", "がい", "cover / lid / canopy", ["ガイ"], ["ふた"]),
        ("目蓋", "まぶた", "eyelids", [], ["まぶた"]),
        ("盆", "ぼん", "tray / Bon Festival / Lantern Festival", ["ボン"], []),
        ("盆地", "ぼんち", "basin (e.g. between mountains)", ["ボンチ"], []),
        ("請負", "うけおい", "contract (for work)", [], ["うけおい"]),
    ],
    # Lesson 307
    [
        ("凶", "きょう", "villain / evil / bad luck / disaster", ["キョウ"], []),
        ("凶作", "きょうさく", "bad harvest / poor crop", ["キョウサク"], []),
        ("裾", "すそ", "hem / skirt / cuff (of trousers) / foot (of a mountain)", ["キョ"], ["すそ"]),
        ("幽す", "ゆうす", "to confine / seclude / shut up", ["ユウ"], ["ゆう.す"]),
        ("逃亡", "とうぼう", "escape / flight / running away / elopement / desertion", ["トウボウ"], []),
    ],
    # Lesson 308
    [
        ("幽霊", "ゆうれい", "ghost / specter / spectre / apparition / phantom", ["ユウレイ"], []),
        ("凡そ", "およそ", "about / roughly / approximately / generally / on the whole", ["ボン", "ハン"], ["およ.そ"]),
        ("凡ゆる", "あらゆる", "all / every", ["ボン", "ハン"], ["あらゆる"]),
        ("平凡", "へいぼん", "ordinary / common / commonplace / mediocre / unremarkable", ["ヘイボン"], []),
        ("埋葬", "まいそう", "burial", ["マイソウ"], []),
    ],
    # Lesson 309
    [
        ("大凡", "おおよそ", "about / roughly / approximately / generally / gist", ["タイボン"], ["おおよそ"]),
        ("暦", "こよみ", "calendar / almanac", ["レキ"], ["こよみ"]),
        ("西暦", "せいれき", "Common Era / CE / Christian Era / AD", ["セイレキ"], []),
        ("腫れる", "はれる", "to swell (from inflammation) / become swollen", ["シュ"], ["は.れる", "は.らす"]),
        ("名残", "なごり", "remains / traces / vestige / reluctance to part", [], ["なごり"]),
    ],
    # Lesson 310
    [
        ("峠", "とうげ", "ridge / (mountain) pass / difficult part / peak / crisis", [], ["とうげ"]),
        ("窮す", "きゅうす", "to be destitute / suffer / be perplexed / be cornered", ["キュウ"], ["きゅう.す"]),
        ("窮乏", "きゅうぼう", "poverty / destitution / privation", ["キュウボウ"], []),
        ("窮屈", "きゅうくつ", "narrow / tight / stiff / rigid / uneasy / constrained", ["キュウクツ"], []),
        ("直感", "ちょっかん", "intuition / instinct / hunch", ["チョッカン"], []),
    ],
    # Lesson 311
    [
        ("擦る", "する", "to rub / chafe / strike (a match) / file / frost (glass)", ["サツ"], ["す.る", "こす.る"]),
        ("擦る", "こする", "to rub / scrub / scrape", ["サツ"], ["こす.る", "す.る"]),
        ("擦れる", "すれる", "to rub / chafe / wear / become sophisticated (cynical)", ["サツ"], ["す.れる"]),
        ("摩擦", "まさつ", "friction / rubbing / chafing / discord", ["マサツ"], []),
        ("道端", "みちばた", "roadside / wayside", [], ["みちばた"]),
    ],
    # Lesson 312
    [
        ("擦れ違い", "すれちがい", "passing each other / missing each other / failing to meet", [], ["すれちがい"]),
        ("稚", "ち", "immature / young", ["チ", "ジ"], ["いとけない", "おさない"]),
        ("幼稚園", "ようちえん", "kindergarten (in Japan, non-compulsory education from age 3)", ["ヨウチエン"], []),
        ("辱め", "はずかしめ", "shame / disgrace / humiliation / insult", ["ジョク"], ["はずかし.め"]),
        ("病む", "やむ", "to fall ill / be ill", ["ビョウ", "ヘイ"], ["や.む", "やまい"]),
    ],
    # Lesson 313
    [
        ("嵐", "あらし", "storm / tempest", ["ラン"], ["あらし"]),
        ("憤り", "いきどおり", "resentment / indignation / wrath / anger", ["フン"], ["いきどお.り"]),
        ("鬱", "うつ", "gloom / depression / melancholy / luxuriant", ["ウツ"], ["うっ.する", "ふさ.ぐ"]),
        ("憂鬱", "ゆううつ", "depression / melancholy / dejection / gloom / despondency", ["ユウウツ"], []),
        ("自ずと", "おのずと", "naturally / as a matter of course", ["ジ", "シ"], ["おの.ずと"]),
    ],
    # Lesson 314
    [
        ("鬱陶しい", "うっとうしい", "gloomy (e.g. mood) / depressing / irritating / troublesome", ["ウットウ"], ["うっとう.しい"]),
        ("疎", "そ", "alienate / rough / neglect / shun / sparse / penetrate", ["ソ", "ショ"], ["うと.い", "うと.む"]),
        ("過疎", "かそ", "depopulation", ["カソ"], []),
        ("雰囲気", "ふんいき", "atmosphere / mood / ambience / aura", ["フンイキ"], []),
        ("雰", "ふん", "atmosphere / fog", ["フン"], []),
    ],
    # Lesson 315
    [
        ("肺", "はい", "lungs", ["ハイ"], []),
        ("拘", "こう", "arrest / seize / concerned / adhere to", ["コウ"], ["かか.わる"]),
        ("拘束", "こうそく", "restriction / restraint / binding / constraint / detention", ["コウソク"], []),
        ("頻りに", "しきりに", "frequently / repeatedly / often / incessantly / constantly", ["ヒン"], ["しき.りに"]),
        ("小僧", "こぞう", "youngster / boy / kid / young Buddhist acolyte / apprentice", ["コゾウ"], []),
    ],
    # Lesson 316
    [
        ("頻繁", "ひんぱん", "frequent / incessant", ["ヒンパン"], []),
        ("豚", "ぶた", "pig (Sus scrofa domesticus) / pork", ["トン"], ["ぶた"]),
        ("豚肉", "ぶたにく", "pork", ["トンニク"], ["ぶたにく"]),
        ("鍛える", "きたえる", "to forge / temper / drill / train / discipline", ["タン"], ["きた.える"]),
        ("弾ける", "はじける", "to burst open / split open / pop", ["ダン"], ["はじ.ける"]),
    ],
    # Lesson 317
    [
        ("繊", "せん", "slender / fine / thin kimono", ["セン"], []),
        ("化繊", "かせん", "synthetic fibers / chemical fibers", ["カセン"], []),
        ("縫う", "ぬう", "to sew / stitch / weave one's way (e.g. through a crowd)", ["ホウ"], ["ぬ.う"]),
        ("裁縫", "さいほう", "sewing / needlework", ["サイホウ"], []),
        ("人質", "ひとじち", "hostage", ["ジンシチ"], ["ひとじち"]),
    ],
    # Lesson 318
    [
        ("把", "は", "grasp / faggot / bunch / counter for bundles", ["ハ", "ワ"], []),
        ("把握", "はあく", "grasp / catch / understanding", ["ハアク"], []),
        ("漬ける", "つける", "to dip in / soak / pickle / preserve (in salt, vinegar, etc.)", ["シ"], ["つ.ける", "つ.かる"]),
        ("紳士服", "しんしふく", "men's clothing / men's wear", ["シンシフク"], []),
        ("紳", "しん", "sire / good belt / gentleman", ["シン"], []),
    ],
    # Lesson 319
    [
        ("飽きる", "あきる", "to get tired of / lose interest in / be fed up with / have enough", ["ホウ"], ["あ.きる", "あ.かす"]),
        ("宛", "あて", "addressed to", ["エン"], ["あ.てる", "-あて"]),
        ("宛てる", "あてる", "to address", ["エン"], ["あ.てる"]),
        ("宛名", "あてな", "recipient's name / address / direction", [], ["あてな"]),
        ("漬物", "つけもの", "tsukemono / Japanese pickled vegetables", [], ["つけもの"]),
    ],
    # Lesson 320
    [
        ("崖", "がけ", "cliff / precipice", ["ガイ", "ゲ", "ギ"], ["がけ"]),
        ("峡", "きょう", "gorge / ravine", ["キョウ", "コウ"], ["はざま"]),
        ("海峡", "かいきょう", "channel (e.g. between two land masses) / strait", ["カイキョウ"], []),
        ("溝", "みぞ", "ditch / drain / gutter / trench / groove / gap", ["コウ"], ["みぞ"]),
        ("差し支える", "さしつかえる", "to interfere / hinder / become impeded", [], ["さしつか.える"]),
    ],
    # Lesson 321
    [
        ("朴", "ぼく", "crude / simple / plain / docile", ["ボク", "ホウ"], ["ほう"]),
        ("瓦", "かわら", "tile", ["ガ"], ["かわら", "ぐらむ"]),
        ("墨", "すみ", "India ink / Chinese ink / ink stick / sumi", ["ボク"], ["すみ"]),
        ("遍", "へん", "everywhere / times / widely / generally", ["ヘン"], ["あまね.く"]),
        ("素朴", "そぼく", "simple / artless / naive / unsophisticated", ["ソボク"], []),
    ],
    # Lesson 322
    [
        ("普遍", "ふへん", "universal / general / ubiquitous / omnipresent", ["フヘン"], []),
        ("濁る", "にごる", "to become muddy / become cloudy / become turbid / become impure", ["ダク", "ジョク"], ["にご.る", "にご.す"]),
        ("清濁", "せいだく", "good and evil / purity and impurity", ["セイダク"], []),
        ("扇ぐ", "あおぐ", "to fan / flap", ["セン"], ["あお.ぐ"]),
        ("一遍", "いっぺん", "one time / once", ["イッペン"], []),
    ],
    # Lesson 323
    [
        ("団扇", "うちわ", "uchiwa / round hand fan", ["ダンセン"], ["うちわ"]),
        ("扇子", "せんす", "folding fan", ["センス"], []),
        ("扇風機", "せんぷうき", "electric fan", ["センプウキ"], []),
        ("じゃん拳", "じゃんけん", "rock-paper-scissors (game)", ["ケン"], ["じゃんけん"]),
        ("賢明", "けんめい", "wise / sensible / well-advised / sagacious", ["ケンメイ"], []),
    ],
    # Lesson 324
    [
        ("堤", "つつみ", "embankment / bank / dike", ["テイ"], ["つつみ"]),
        ("堤防", "ていぼう", "bank / weir / embankment / levee", ["テイボウ"], []),
        ("阻む", "はばむ", "to keep someone from doing / stop / prevent / check / hinder", ["ソ"], ["はば.む"]),
        ("虜", "とりこ", "captive / prisoner / victim / slave", ["リョ", "ロ"], ["とりこ", "とりく"]),
        ("阻害", "そがい", "obstruction / inhibition / hindrance / blocking", ["ソガイ"], []),
    ],
    # Lesson 325
    [
        ("捕虜", "ほりょ", "prisoner (of war)", ["ホリョ"], []),
        ("鐘", "かね", "bell (often a large hanging bell) / chime", ["ショウ"], ["かね"]),
        ("剰", "じょう", "surplus / besides", ["ジョウ"], ["あまつさえ", "あま.り"]),
        ("径", "けい", "diameter / path / method", ["ケイ"], ["みち", "こみち"]),
        ("過剰", "かじょう", "excess / over-", ["カジョウ"], []),
    ],
    # Lesson 326
    [
        ("直径", "ちょっけい", "diameter", ["チョッケイ"], []),
        ("半径", "はんけい", "radius", ["ハンケイ"], []),
        ("培う", "つちかう", "to cultivate / foster / nurture", ["バイ"], ["つちか.う"]),
        ("砕く", "くだく", "to break / smash", ["サイ"], ["くだ.く", "くだ.ける"]),
        ("建立", "こんりゅう", "act of building (temple, monument, etc.) / erection", ["コンリュウ"], []),
    ],
    # Lesson 327
    [
        ("砕ける", "くだける", "to break (into pieces) / be broken / be smashed / collapse", ["サイ"], ["くだ.ける"]),
        ("絹", "きぬ", "silk", ["ケン"], ["きぬ"]),
        ("譜", "ふ", "musical score / music / note / staff / table / genealogy", ["フ"], []),
        ("陵", "みささぎ", "mausoleum / imperial tomb / hill / mound", ["リョウ"], ["みささぎ"]),
        ("懐中", "かいちゅう", "one's pocket", ["カイチュウ"], []),
    ],
    # Lesson 328
    [
        ("丘陵", "きゅうりょう", "hill / hillock", ["キュウリョウ"], []),
        ("痴", "ち", "stupid / foolish", ["チ"], ["し.れる", "おろか"]),
        ("愚痴", "ぐち", "idle complaint / grumble", ["グチ"], []),
        ("笛", "ふえ", "flute / fife / pipe / recorder / whistle", ["テキ"], ["ふえ"]),
        ("辛抱", "しんぼう", "patience / endurance", ["シンボウ"], []),
    ],
    # Lesson 329
    [
        ("唾", "つば", "saliva / spit / sputum", ["ダ", "タ"], ["つば", "つばき"]),
        ("塀", "へい", "wall / fence", ["ヘイ", "ベイ"], []),
        ("碁", "ご", "Go (board game of capturing territory)", ["ゴ"], []),
        ("碁盤", "ごばん", "Go board", ["ゴバン"], []),
        ("束の間", "つかのま", "moment / brief time / brief / fleeting / transient", [], ["つかのま"]),
    ],
    # Lesson 330
    [
        ("敢えて", "あえて", "purposely / daringly (to do something) / boldly", ["カン"], ["あ.えて"]),
        ("胴", "どう", "trunk / torso / hull (ship) / hub / frame", ["ドウ"], []),
        ("謡", "うたい", "noh chanting / song / ballad", ["ヨウ"], ["うたい", "うた.う"]),
        ("民謡", "みんよう", "folk song / popular song", ["ミンヨウ"], []),
        ("出費", "しゅっぴ", "expenses / disbursements / expenditure", ["シュッピ"], []),
    ],
    # Lesson 331
    [
        ("歌謡", "かよう", "song / ballad", ["カヨウ"], []),
        ("飢える", "うえる", "to starve / famish / be hungry / be starved of (e.g. love)", ["キ"], ["う.える"]),
        ("欄", "らん", "column of text (e.g. as in a newspaper) / field / blank", ["ラン"], ["てすり"]),
        ("艶", "つや", "gloss / luster / lustre / glaze / sheen / charm", ["エン"], ["つや", "なま.めかしい"]),
        ("弾丸", "だんがん", "bullet / shot / shell", ["ダンガン"], []),
    ],
    # Lesson 332
    [
        ("怠ける", "なまける", "to be idle / slacken / be lazy / neglect (one's work, etc.)", ["タイ"], ["なま.ける", "おこた.る"]),
        ("欺く", "あざむく", "to deceive / delude / trick / fool", ["ギ"], ["あざむ.く"]),
        ("泡", "あわ", "bubble / foam / froth / head on beer", ["ホウ"], ["あわ"]),
        ("諦める", "あきらめる", "to give up / abandon (hope, plans) / resign oneself (to)", ["テイ", "タイ"], ["あきら.める"]),
        ("怠る", "おこたる", "to be negligent in doing something / shirk / be off one's guard", ["タイ"], ["おこた.る"]),
    ],
    # Lesson 333
    [
        ("餅", "もち", "mochi / sticky rice cake", ["ヘイ", "ヒョウ"], ["もち"]),
        ("寮", "りょう", "hostel / dormitory", ["リョウ"], []),
        ("厄", "やく", "unlucky / misfortune / bad luck / disaster", ["ヤク"], []),
        ("厄介", "やっかい", "trouble / burden / nuisance / bother / care / kindness", ["ヤッカイ"], []),
        ("堪能", "たんのう", "proficient / skillful / versed / satisfied / having one's fill", ["タンノウ", "カンノウ"], []),
    ],
    # Lesson 334
    [
        ("瞳", "ひとみ", "pupil (of eye) / one's eyes", ["ドウ", "トウ"], ["ひとみ"]),
        ("渦", "うず", "swirl / eddy / whirlpool / vortex", ["カ"], ["うず"]),
        ("襟", "えり", "collar / lapel / neckband / neck", ["キン"], ["えり"]),
        ("吟じる", "ぎんじる", "to sing / chant / recite", ["ギン"], ["ぎん.じる"]),
        ("朗読", "ろうどく", "reading aloud / recitation", ["ロウドク"], []),
    ],
    # Lesson 335
    [
        ("吟味", "ぎんみ", "testing / scrutiny / careful investigation / close examination", ["ギンミ"], []),
        ("トロイ衡", "トロイこう", "troy weight", ["コウ"], []),
        ("呈す", "ていす", "to show / display / exhibit / present / offer", ["テイ"], ["てい.す"]),
        ("進呈", "しんてい", "presentation (e.g. of a gift)", ["シンテイ"], []),
        ("紫陽花", "あじさい", "hydrangea (Hydrangea macrophylla)", [], ["あじさい"]),
    ],
    # Lesson 336
    [
        ("隙", "すき", "gap / space / break / chink / aperture / chance / opportunity", ["ゲキ", "キャク"], ["すき", "す.く"]),
        ("隙間", "すきま", "crevice / crack / gap / opening / clearance", [], ["すきま"]),
        ("懲りる", "こりる", "to learn by experience / be disgusted with / learn one's lesson", ["チョウ"], ["こ.りる", "こ.らす"]),
        ("幣", "へい", "cash / bad habit / humble prefix / gift / Shinto offerings", ["ヘイ"], ["ぬさ"]),
        ("懲役", "ちょうえき", "penal servitude / imprisonment with hard labor", ["チョウエキ"], []),
    ],
    # Lesson 337
    [
        ("紙幣", "しへい", "paper money / notes / bills", ["シヘイ"], []),
        ("箇", "か", "counter for articles", ["カ", "コ"], []),
        ("醜い", "みにくい", "ugly / unattractive / unsightly / unseemly", ["シュウ"], ["みにく.い", "しこ"]),
        ("箸", "はし", "chopsticks", ["チョ"], ["はし"]),
        ("乙女", "おとめ", "virgin / maiden / young girl", [], ["おとめ"]),
    ],
    # Lesson 338
    [
        ("親戚", "しんせき", "relative / relation / kin", ["シンセキ"], []),
        ("紺", "こん", "dark blue / navy", ["コン"], []),
        ("鋼", "はがね", "steel", ["コウ"], ["はがね"]),
        ("鉄鋼", "てっこう", "iron and steel", ["テッコウ"], []),
        ("戒", "かい", "commandment", ["カイ"], ["いまし.める"]),
    ],
    # Lesson 339
    [
        ("褒める", "ほめる", "to praise / admire / speak well of", ["ホウ"], ["ほ.める"]),
        ("赴く", "おもむく", "to go in the direction of / proceed toward / become", ["フ"], ["おもむ.く"]),
        ("赴任", "ふにん", "moving to a different location to start a new job", ["フニン"], []),
        ("妬む", "ねたむ", "to be jealous of / envy / begrudge", ["ト", "ツ"], ["ねた.む", "そね.む"]),
        ("火傷", "やけど", "burn / scald", ["カショウ"], ["やけど"]),
    ],
    # Lesson 340
    [
        ("遮る", "さえぎる", "to interrupt / obstruct (a view, etc.) / block (light, wind, etc.)", ["シャ"], ["さえぎ.る"]),
        ("釜", "かま", "iron pot / kettle", ["フ"], ["かま"]),
        ("茎", "くき", "stalk / stem", ["ケイ", "キョウ"], ["くき"]),
        ("蔑む", "さげすむ", "to scorn / disdain / look down on / despise", ["ベツ"], ["さげす.む"]),
        ("遮断", "しゃだん", "isolation / interruption / cutting off / blocking", ["シャダン"], []),
    ],
    # Lesson 341
    [
        ("軽蔑", "けいべつ", "scorn / disdain / contempt", ["ケイベツ"], []),
        ("嗅ぐ", "かぐ", "to sniff / smell", ["キュウ"], ["か.ぐ"]),
        ("蜜", "みつ", "honey / nectar / molasses / treacle", ["ミツ", "ビツ"], []),
        ("戴きます", "いただきます", "thank you for the meal (before eating) / I humbly receive", ["タイ"], ["いただ.きます"]),
        ("頂戴", "ちょうだい", "receiving / getting / accepting / please / please give me", ["チョウダイ"], []),
    ],
    # Lesson 342
    [
        ("宜しく", "よろしく", "well / properly / suitably / best regards / please remember me", ["ギ"], ["よろ.しく"]),
        ("宜しい", "よろしい", "good / OK / all right / fine / very well / may", ["ギ"], ["よろ.しい"]),
        ("どうぞ宜しく", "どうぞよろしく", "pleased to meet you / please remember me / best regards", ["ギ"], ["どうぞよろ.しく"]),
        ("便宜", "べんぎ", "convenience / accommodation / advantage / expediency", ["ベンギ"], []),
        ("縁起", "えんぎ", "omen / luck / origin / history", ["エンギ"], []),
    ],
    # Lesson 343
    [
        ("適宜", "てきぎ", "suitably / accordingly / as occasion demands / at one's discretion", ["テキギ"], []),
        ("殻", "から", "shell / husk / hull / pod / chaff", ["カク", "コク", "バイ"], ["から", "がら"]),
        ("貝殻", "かいがら", "seashell / shell", [], ["かいがら"]),
        ("炊く", "たく", "to boil (rice) / cook", ["スイ"], ["た.く"]),
        ("梅干", "うめぼし", "umeboshi / dried and pickled ume", [], ["うめぼし"]),
    ],
    # Lesson 344
    [
        ("自炊", "じすい", "cooking for oneself / making one's own food", ["ジスイ"], []),
        ("炊飯器", "すいはんき", "rice cooker", ["スイハンキ"], []),
        ("碑", "ひ", "tombstone / monument", ["ヒ"], ["いしぶみ"]),
        ("痩せる", "やせる", "to become thin / lose weight / slim", ["ソウ", "シュウ"], ["や.せる"]),
        ("一変", "いっぺん", "complete change / about-face", ["イッペン"], []),
    ],
    # Lesson 345
    [
        ("但し", "ただし", "but / however / provided that", ["タン"], ["ただ.し"]),
        ("奨学金", "しょうがくきん", "scholarship / stipend / student loan", ["ショウガクキン"], []),
        ("薦", "せん", "recommend / mat / advise / encourage / offer", ["セン"], ["すす.める"]),
        ("閑", "かん", "leisure", ["カン"], []),
        ("奨", "しょう", "exhort / urge / encourage", ["ショウ", "ソウ"], ["すす.める"]),
    ],
    # Lesson 346
    [
        ("長閑", "のどか", "tranquil / calm / quiet / peaceful / serence", ["チョウカン"], ["のどか"]),
        ("錠", "じょう", "lock / fetters / shackles / pill", ["ジョウ"], []),
        ("手錠", "てじょう", "handcuffs / manacles", ["テジョウ"], []),
        ("妨げる", "さまたげる", "to disturb / prevent / obstruct / hinder", ["ボウ"], ["さまた.げる"]),
        ("推薦", "すいせん", "recommendation / referral / endorsement", ["スイセン"], []),
    ],
    # Lesson 347
    [
        ("妨害", "ぼうがい", "disturbance / obstruction / hindrance / jamming / interference", ["ボウガイ"], []),
        ("蜂", "はち", "bee / wasp / hornet", ["ホウ"], ["はち"]),
        ("蜂蜜", "はちみつ", "honey", ["ハチミツ"], []),
        ("弄る", "いじる", "to finger / touch / play with / fiddle with / tamper with", ["ロウ"], ["いじ.る", "もてあそ.ぶ"]),
        ("家来", "けらい", "retainer / retinue / servant", ["ケライ"], []),
    ],
    # Lesson 348
    [
        ("罵る", "ののしる", "to speak ill of / abuse / rail at / swear at / curse", ["バ"], ["ののし.る"]),
        ("鉛", "なまり", "lead (the metal)", ["エン"], ["なまり"]),
        ("鉛筆", "えんぴつ", "pencil", ["エンピツ"], []),
        ("璧", "へき", "sphere / jewel / perfect", ["ヘキ"], ["たま"]),
        ("完璧", "かんぺき", "perfect / complete / flawless", ["カンペキ"], []),
    ],
    # Lesson 349
    [
        ("歌舞伎", "かぶき", "kabuki (Japanese classical drama)", ["カブキ"], []),
        ("曖昧", "あいまい", "vague / ambiguous / unclear / fuzzy", ["アイマイ"], []),
        ("餌", "えさ", "(animal) feed / fodder / pet food / bait / lure", ["ジ", "ニ"], ["えさ", "えば"]),
        ("岬", "みさき", "cape (on coast)", ["コウ"], ["みさき"]),
        ("伎", "ぎ", "deed / skill", ["ギ", "キ"], ["わざ"]),
    ],
    # Lesson 350
    [
        ("暫く", "しばらく", "for a moment / for a minute / for a while / for some time", ["ザン"], ["しばら.く"]),
        ("爽やか", "さわやか", "fresh / refreshing / invigorating / clear / fluent", ["ソウ"], ["さわ.やか"]),
        ("諾", "だく", "consent / assent / agreement", ["ダク"], []),
        ("承諾", "しょうだく", "consent / approval / acceptance / agreement / compliance", ["ショウダク"], []),
        ("暫定", "ざんてい", "provisional / temporary / tentative", ["ザンテイ"], []),
    ],
    # Lesson 351
    [
        ("芯", "しん", "wick / marrow / staple (for stapler) / core / heart / center", ["シン"], []),
        ("綻びる", "ほころびる", "to come apart at the seams / be ripped / begin to open / smile broadly", ["タン"], ["ほころ.びる"]),
        ("訂", "てい", "revise / correct / decide", ["テイ"], []),
        ("改訂", "かいてい", "revision (of text)", ["カイテイ"], []),
        ("破綻", "はたん", "failure / collapse / breakdown / bankruptcy", ["ハタン"], []),
    ],
    # Lesson 352
    [
        ("俵", "たわら", "straw bag / bale / sack / counter for bags", ["ヒョウ"], ["たわら"]),
        ("土俵", "どひょう", "sumo ring / arena", ["ドヒョウ"], []),
        ("枢", "すう", "hinge / pivot / door", ["スウ", "シュ"], ["とぼそ", "からくり"]),
        ("肘", "ひじ", "elbow", ["チュウ"], ["ひじ"]),
        ("中枢", "ちゅうすう", "center / pivot / mainstay / nucleus / backbone", ["チュウスウ"], []),
    ],
    # Lesson 353
    [
        ("麓", "ふもと", "foot (of a mountain or hill) / bottom / base", ["ロク"], ["ふもと"]),
        ("憧れ", "あこがれ", "yearning / longing / aspiration / adoration / admiration", ["ショウ"], ["あこが.れ"]),
        ("憧れる", "あこがれる", "to long for / yearn after / admire / be attracted by", ["ショウ"], ["あこが.れる"]),
        ("酌む", "くむ", "to serve sake / draw (water) / dip / ladle / drink together", ["シャク"], ["く.む"]),
        ("背く", "そむく", "to run counter to / go against / disobey / infringe", ["ハイ"], ["そむ.く"]),
    ],
    # Lesson 354
    [
        ("渇く", "かわく", "to be thirsty / feel thirsty", ["カツ"], ["かわ.く"]),
        ("喉が渇く", "のどがかわく", "to be thirsty", [], ["のどがかわ.く"]),
        ("慕う", "したう", "to yearn for / miss / adore / love dearly", ["ボ"], ["した.う"]),
        ("婿", "むこ", "husband / groom / (one's) son-in-law", ["セイ"], ["むこ"]),
        ("屈辱", "くつじょく", "disgrace / humiliation", ["クツジョク"], []),
    ],
    # Lesson 355
    [
        ("慨する", "がいする", "to lament / deplore / be indignant", ["ガイ"], ["がい.する"]),
        ("感慨", "かんがい", "deep emotion / strong feeling", ["カンガイ"], []),
        ("憤慨", "ふんがい", "indignation / resentment", ["フンガイ"], []),
        ("侮", "ぶ", "scorn / despise / make light of / contempt", ["ブ"], ["あなど.る"]),
        ("雨水", "あまみず", "rainwater", ["ウスイ"], ["あまみず"]),
    ],
    # Lesson 356
    [
        ("該", "がい", "above-stated / the said / that specific", ["ガイ"], []),
        ("該当", "がいとう", "corresponding (to) / being applicable / coming under", ["ガイトウ"], []),
        ("臆す", "おくす", "to fear / hesitate / be nervous / feel timid", ["オク", "ヨク"], ["おく.す"]),
        ("臆病", "おくびょう", "cowardly / timid / easily frightened", ["オクビョウ"], []),
        ("切開", "せっかい", "incision / section / operation / cutting open", ["セッカイ"], []),
    ],
    # Lesson 357
    [
        ("桟", "さん", "scaffold / cleat / frame / jetty / bolt (door)", ["サン", "セン"], ["かけはし"]),
        ("溺れる", "おぼれる", "to drown / sink / indulge in / lose one's head over", ["デキ"], ["おぼ.れる"]),
        ("賄う", "まかなう", "to supply (goods, money, etc.) / cover (costs) / pay / finance / feed", ["ワイ"], ["まかな.う"]),
        ("滑稽", "こっけい", "funny / comical / humorous / laughable / ridiculous", ["コッケイ"], []),
        ("産卵", "さんらん", "egg-laying / spawning", ["サンラン"], []),
    ],
    # Lesson 358
    [
        ("汽", "き", "vapor / steam", ["キ"], []),
        ("汽車", "きしゃ", "train (esp. long distance train)", ["キシャ"], []),
        ("昭", "しょう", "shining / bright", ["ショウ"], []),
        ("昭和", "しょうわ", "Showa era (1926.12.25-1989.1.7)", ["ショウワ"], []),
        ("苛立ち", "いらだち", "irritation / exasperation / impatience", ["カ"], ["いらだ.ち"]),
    ],
    # Lesson 359
    [
        ("佐", "さ", "assistant / help", ["サ"], []),
        ("補佐", "ほさ", "aid / help / assistance / assistant / counselor / adviser", ["ホサ"], []),
        ("媛", "ひめ", "beautiful woman / princess", ["エン"], ["ひめ"]),
        ("岐", "き", "branch off / fork in road / scene / arena / theater", ["キ", "ギ"], []),
        ("大綱", "たいこう", "fundamental principles / main lines / general rules / outline", ["タイコウ"], []),
    ],
    # Lesson 360
    [
        ("多岐", "たき", "many branches / wide-ranging / diverse / many-sided", ["タキ"], []),
        ("梨", "なし", "nashi (Pyrus pyrifolia, esp. var. culta) / Japanese pear", ["リ"], ["なし"]),
        ("滋", "じ", "nourishing / more & more / be luxuriant / planting / turbidity", ["ジ"], []),
        ("滋養", "じよう", "nourishment / nutrition", ["ジヨウ"], []),
        ("面倒臭い", "めんどうくさい", "bothersome / tiresome / bother to do", [], ["めんどうくさ.い"]),
    ],
    # Lesson 361
    [
        ("潟", "かた", "lagoon", ["セキ"], ["かた", "-がた"]),
        ("熊", "くま", "bear", ["ユウ"], ["くま"]),
        ("衛", "えい", "defense / protection", ["エイ", "エ"], []),
        ("自衛隊", "じえいたい", "Japan Self-Defense Forces / JSDF", ["ジエイタイ"], []),
        ("衛星", "えいせい", "satellite (natural or artificial)", ["エイセイ"], []),
    ],
    # Lesson 362
    [
        ("仁", "じん", "humanity / virtue / benevolence / charity / man / kernel", ["ジン", "ニ", "ニン"], []),
        ("創", "そう", "genesis / wound / injury / hurt / start / originate", ["ソウ", "ショウ"], ["つく.る", "はじ.める"]),
        ("創設", "そうせつ", "establishment / founding / organization", ["ソウセツ"], []),
        ("后", "こう", "empress / queen / after / behind / back / later", ["コウ", "ゴ"], ["きさき"]),
        ("新潟", "にいがた", "Niigata", [], ["にいがた"]),
    ],
    # Lesson 363
    [
        ("尺", "しゃく", "shaku (traditional unit of length, approx. 30.3 cm) / measure", ["シャク"], []),
        ("憲", "けん", "constitution / law", ["ケン"], []),
        ("憲法", "けんぽう", "constitution", ["ケンポウ"], []),
        ("批", "ひ", "criticism / strike", ["ヒ"], []),
        ("熊本", "くまもと", "Kumamoto", [], ["くまもと"]),
    ],
    # Lesson 364
    [
        ("批判", "ひはん", "criticism / judgement / judgment / comment", ["ヒハン"], []),
        ("拡", "かく", "broaden / extend / expand / enlarge", ["カク", "コウ"], ["ひろ.がる", "ひろ.げる"]),
        ("拡大", "かくだい", "magnification / enlargement / expansion / amplification", ["カクダイ"], []),
        ("揮", "き", "brandish / wave / wag / swing / shake", ["キ"], ["ふる.う"]),
        ("劣化", "れっか", "deterioration / degradation / degeneration", ["レッカ"], []),
    ],
    # Lesson 365
    [
        ("指揮", "しき", "command / direction / supervision / conducting (an orchestra)", ["シキ"], []),
        ("樹", "じゅ", "timber / trees / wood / establish / set up", ["ジュ"], ["き"]),
        ("樹立", "じゅりつ", "establishment / founding / setting (a record)", ["ジュリツ"], []),
        ("皇", "こう", "emperor", ["コウ", "オウ"], []),
        ("皇后", "こうごう", "(Japanese) empress / queen", ["コウゴウ"], []),
    ],
    # Lesson 366
    [
        ("天皇", "てんのう", "Emperor of Japan", ["テンノウ"], []),
        ("盟", "めい", "alliance / oath", ["メイ"], []),
        ("加盟", "かめい", "joining (an association, agreement, etc.) / participation / affiliation", ["カメイ"], []),
        ("磁", "じ", "magnet / porcelain", ["ジ"], []),
        ("熱狂", "ねっきょう", "wild enthusiasm / craze / mania / frenzy", ["ネッキョウ"], []),
    ],
    # Lesson 367
    [
        ("磁気", "じき", "magnetism", ["ジキ"], []),
        ("穀", "こく", "cereals / grain", ["コク"], []),
        ("穀物", "こくもつ", "grain / cereal / corn", ["コクモツ"], []),
        ("蚕", "かいこ", "silkworm", ["サン"], ["かいこ", "こ"]),
        ("大雑把", "おおざっぱ", "rough (not precise) / broad / sketchy", [], ["おおざっぱ"]),
    ],
    # Lesson 368
    [
        ("閣", "かく", "tower / tall building / palace / cabinet", ["カク"], []),
        ("閣僚", "かくりょう", "cabinet ministers", ["カクリョウ"], []),
        ("陛", "へい", "highness / steps (of throne)", ["ヘイ"], []),
        ("陛下", "へいか", "Your Majesty / His Majesty / Her Majesty", ["ヘイカ"], []),
        ("描ける", "えがける", "can draw / can paint / can depict", ["ビョウ"], ["えが.ける"]),
    ],
    # Lesson 369
    [
        ("且つ", "かつ", "yet / and / moreover / besides / as well as", ["ショ"], ["か.つ"]),
        ("丙", "へい", "third class / 3rd / 3rd calendar sign", ["ヘイ"], ["ひのえ"]),
        ("丹", "たん", "rust-colored / red / red lead / pills / sincerity", ["タン"], ["に"]),
        ("丹念", "たんねん", "elaborate / painstaking / diligent / careful", ["タンネン"], []),
        ("鞄", "かばん", "bag / satchel / briefcase / basket", ["ハク", "ホウ", "ビョウ"], ["かばん"]),
    ],
    # Lesson 370
    [
        ("亀", "かめ", "tortoise / turtle", ["キ", "キュウ", "キン"], ["かめ"]),
        ("享", "きょう", "enjoy / receive / undergo / answer (phone) / take / get / catch", ["キョウ", "コウ"], ["う.ける"]),
        ("享受", "きょうじゅ", "reception / acceptance / enjoyment / being given", ["キョウジュ"], []),
        ("亭", "てい", "pavilion / restaurant / mansion / arbor / cottage / vaudeville", ["テイ", "チン"], []),
        ("中堅", "ちゅうけん", "nucleus / backbone / mainstay / key figure / medium-sized", ["チュウケン"], []),
    ],
    # Lesson 371
    [
        ("料亭", "りょうてい", "high-class traditional Japanese restaurant", ["リョウテイ"], []),
        ("伐", "ばつ", "fell / strike / attack / punish", ["バツ", "ハツ", "カ"], ["き.る", "そむ.く"]),
        ("伐採", "ばっさい", "felling timber / cutting down trees / logging / lumbering", ["バッサイ"], []),
        ("併", "へい", "join / get together / unite / collective", ["ヘイ"], ["あわ.せる"]),
        ("仕業", "しわざ", "deed / act / action / work", [], ["しわざ"]),
    ],
    # Lesson 372
    [
        ("合併", "がっぺい", "combination / union / amalgamation / consolidation / merger", ["ガッペイ"], []),
        ("侯", "こう", "marquis / lord / daimyo", ["コウ"], []),
        ("俊", "しゅん", "sagacious / genius / excellence", ["シュン"], []),
        ("俊足", "しゅんそく", "fleet steed / fast runner / swift-footedness / genius", ["シュンソク"], []),
        ("鳥獣", "ちょうじゅう", "birds and beasts / wildlife", ["チョウジュウ"], []),
    ],
    # Lesson 373
    [
        ("俸", "ほう", "stipend / salary", ["ホウ"], []),
        ("年俸", "ねんぽう", "annual salary", ["ネンポウ"], []),
        ("倣う", "ならう", "to imitate / follow / emulate", ["ホウ"], ["なら.う"]),
        ("倫", "りん", "ethics / companion", ["リン"], []),
        ("匹敵", "ひってき", "comparing with / matching / rivaling / equaling", ["ヒッテキ"], []),
    ],
    # Lesson 374
    [
        ("倫理", "りんり", "ethics / morals", ["リンリ"], []),
        ("倹", "けん", "frugal / economy / thrifty", ["ケン"], ["つま.しい", "つづまやか"]),
        ("倹約", "けんやく", "thrift / economy / frugality", ["ケンヤク"], []),
        ("偵", "てい", "spy", ["テイ"], []),
        ("探偵", "たんてい", "detective / sleuth / investigator / detective work", ["タンテイ"], []),
    ],
    # Lesson 375
    [
        ("偵察", "ていさつ", "scouting / reconnaissance", ["テイサツ"], []),
        ("傑", "けつ", "greatness / excellence", ["ケツ"], ["すぐ.れる"]),
        ("傑作", "けっさく", "masterpiece / best work / blunder / boner", ["ケッサク"], []),
        ("儒", "じゅ", "Confucian", ["ジュ"], []),
        ("謙虚", "けんきょ", "modest / humble", ["ケンキョ"], []),
    ],
    # Lesson 376
    [
        ("儒教", "じゅきょう", "Confucianism", ["ジュキョウ"], []),
        ("克", "こく", "overcome / kindly / skillfully", ["コク"], ["か.つ"]),
        ("克服", "こくふく", "subjugation / conquest / overcoming (a difficulty, illness, etc.)", ["コクフク"], []),
        ("冶", "や", "melting / smelting", ["ヤ"], ["い.る"]),
        ("途絶える", "とだえる", "to stop / cease / come to an end / break off", [], ["とだ.える"]),
    ],
]


def get_strokes_for_char(ch: str) -> list[str]:
    hex_code = f"{ord(ch):05x}"
    svg_path = os.path.join(KANJIVG_DIR, f"{hex_code}.svg")
    if not os.path.exists(svg_path):
        print(f"WARNING: Missing SVG for '{ch}' ({hex_code}.svg)")
        return []
    tree = ET.parse(svg_path)
    root = tree.getroot()
    strokes = []
    for elem in root.iter():
        if elem.tag.endswith("path"):
            d = elem.attrib.get("d")
            if d:
                strokes.append(d.strip())
    return strokes


def main():
    if not os.path.exists(PART2_JSON_PATH):
        raise FileNotFoundError(f"Run 'python generate_n1_part2.py' first to create {PART2_JSON_PATH}.")

    with open(PART2_JSON_PATH, "r", encoding="utf-8") as f:
        lessons = json.load(f)

    item_counter = sum(len(l["items"]) for l in lessons) + 1

    for l_idx, chunk in enumerate(N1_PART3_DATA):
        lesson_num = 251 + l_idx
        lesson_items = []

        for word, kana, meaning, onyomi, kunyomi in chunk:
            characters_data = []
            for ch in word:
                characters_data.append({
                    "char": ch,
                    "strokes": get_strokes_for_char(ch),
                })

            lesson_items.append({
                "id": f"n1-{item_counter}",
                "level": "N1",
                "word": word,
                "kana": kana,
                "meaning": meaning,
                "onyomi": onyomi,
                "kunyomi": kunyomi,
                "characters": characters_data,
            })
            item_counter += 1

        lessons.append({
            "id": f"n1-lesson-{lesson_num}",
            "level": "N1",
            "lessonNumber": lesson_num,
            "items": lesson_items,
        })

    with open(PART3_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(lessons, f, ensure_ascii=False)

    print(f"Part 3 complete! Saved Lessons 1-376 ({item_counter - 1} items) to {PART3_JSON_PATH}.")


if __name__ == "__main__":
    main()