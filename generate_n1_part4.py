import os
import json
import xml.etree.ElementTree as ET

KANJIVG_DIR = "kanjivg-data"
PART3_JSON_PATH = "n1_part3.json"
PART4_JSON_PATH = "n1_part4.json"

N1_PART4_DATA = [
    # Lesson 377
    [
        ("冶金", "やきん", "metallurgy", ["ヤキン"], []),
        ("に準じて", "にじゅんじて", "according to / in proportion to", ["ジュン"], []),
        ("批准", "ひじゅん", "ratification", ["ヒジュン"], []),
        ("凸", "とつ", "convex / beetle brow / uneven", ["トツ"], ["でこ"]),
        ("静寂", "せいじゃく", "silence / stillness / quietness", ["セイジャク"], []),
    ],
    # Lesson 378
    [
        ("凸版印刷", "とっぱんいんさつ", "letterpress printing / relief printing", ["トッパンインサツ"], []),
        ("凹", "おう", "concave / hollow / sunken", ["オウ"], ["くぼ.む", "へこ.む", "ぼこ"]),
        ("凹凸", "おうとつ", "unevenness / roughness / ruggedness", ["オウトツ"], ["でこぼこ"]),
        ("剖", "ぼう", "divide", ["ボウ", "ホウ"], []),
        ("凹む", "へこむ", "to be dented / be indented / yield / feel down", ["オウ"], ["へこ.む", "くぼ.む"]),
    ],
    # Lesson 379
    [
        ("解剖", "かいぼう", "dissection / autopsy / analysis", ["カイボウ"], []),
        ("剛", "ごう", "sturdy / strength", ["ゴウ"], []),
        ("金剛", "こんごう", "diamond / adamantine / strength", ["コンゴウ"], []),
        ("劾", "がい", "censure / criminal investigation", ["ガイ"], []),
        ("玄米", "げんまい", "unpolished rice / brown rice", ["ゲンマイ"], []),
    ],
    # Lesson 380
    [
        ("弾劾", "だんがい", "impeachment / accusation / censure", ["ダンガイ"], []),
        ("勅", "ちょく", "imperial order", ["チョク"], ["みことのり"]),
        ("勲", "くん", "meritorious deed / merit / order of merit", ["クン"], ["いさお"]),
        ("勲章", "くんしょう", "decoration / order / medal", ["クンショウ"], []),
        ("老舗", "しにせ", "old-established shop / store of long standing", [], ["しにせ"]),
    ],
    # Lesson 381
    [
        ("匠", "たくみ", "artisan / workman / carpenter", ["ショウ"], ["たくみ"]),
        ("匿", "とく", "hide / shelter / shield", ["トク"], ["かくま.う"]),
        ("匿名", "とくめい", "anonymity / pseudonym", ["トクメイ"], []),
        ("升", "ます", "measuring box / 1.8 liter measure", ["ショウ"], ["ます"]),
        ("師匠", "ししょう", "master / teacher", ["シショウ"], []),
    ],
    # Lesson 382
    [
        ("卸", "おろし", "wholesale", ["シャ"], ["おろ.す", "おろし"]),
        ("厘", "りん", "rin / one-tenth of a sen / one-thousandth", ["リン"], []),
        ("叙", "じょ", "confer / relate / narrate / describe", ["ジョ"], ["つい.ず", "ついで"]),
        ("叙情", "じょじょう", "lyricism / description of feelings", ["ジョジョウ"], []),
        ("恐慌", "きょうこう", "panic / scare / consternation / financial crisis", ["キョウコウ"], []),
    ],
    # Lesson 383
    [
        ("吏", "り", "officer / an official", ["リ"], []),
        ("官吏", "かんり", "government official", ["カンリ"], []),
        ("唄", "うた", "song / ballad (with shamisen accompaniment)", ["バイ"], ["うた"]),
        ("長唄", "ながうた", "nagauta (traditional epic song in kabuki)", [], ["ながうた"]),
        ("平穏", "へいおん", "tranquil / calm / quiet / peaceful", ["ヘイオン"], []),
    ],
    # Lesson 384
    [
        ("唆", "そそのかす", "to tempt / seduce / instigate / promote", ["サ"], ["そそのか.す"]),
        ("示唆", "しさ", "suggestion / hint / implication", ["シサ"], []),
        ("唐", "から", "Tang (dynasty of China) / China / foreign", ["トウ"], ["から"]),
        ("喚く", "わめく", "to shout / cry / scream / clamor", ["カン"], ["わめ.く"]),
        ("唐辛子", "とうがらし", "capsicum / cayenne / chili pepper", ["トウガラシ"], []),
    ],
    # Lesson 385
    [
        ("喚問", "かんもん", "summons (e.g. to parliament)", ["カンモン"], []),
        ("喝", "かつ", "hoarse / scold", ["カツ"], []),
        ("恐喝", "きょうかつ", "threat / blackmail / extortion", ["キョウカツ"], []),
        ("喪", "も", "mourning", ["ソウ"], ["も"]),
        ("側近", "そっきん", "close associate / aide / brain truster", ["ソッキン"], []),
    ],
    # Lesson 386
    [
        ("嗣", "し", "heir / succeed", ["シ"], ["つ.ぐ"]),
        ("嘱", "しょく", "entrust / request / send a message", ["ショク"], ["しょく.する", "たの.む"]),
        ("嘱託", "しょくたく", "part-time employee / commission / entrusting", ["ショクタク"], []),
        ("噴く", "ふく", "to spout / emit / flush / erupt", ["フン"], ["ふ.く"]),
        ("窓際", "まどぎわ", "by the window / window-side", [], ["まどぎわ"]),
    ],
    # Lesson 387
    [
        ("噴火", "ふんか", "eruption / volcanic eruption", ["フンカ"], []),
        ("嚇す", "おどす", "to threaten / menace / frighten", ["カク"], ["おど.す"]),
        ("威嚇", "いかく", "threat / intimidation / menace", ["イカク"], []),
        ("囚", "しゅう", "captured / criminal / arrest / catch", ["シュウ"], ["とら.われる"]),
        ("石器", "せっき", "stone implement / stoneware", ["セッキ"], []),
    ],
    # Lesson 388
    [
        ("死刑囚", "しけいしゅう", "prisoner condemned to death / death row inmate", ["シケイシュウ"], []),
        ("坑", "こう", "pit / hole", ["コウ"], []),
        ("坑内", "こうない", "inside a mine / pit", ["コウナイ"], []),
        ("坪", "つぼ", "two-mat area (~3.31 sq meters)", ["ヘイ"], ["つぼ"]),
        ("多忙", "たぼう", "being very busy / pressure of work", ["タボウ"], []),
    ],
    # Lesson 389
    [
        ("堕", "だ", "degenerate / descend to / lapse into", ["ダ"], ["お.ちる", "くず.す"]),
        ("堕落", "だらく", "depravity / corruption / degradation", ["ダラク"], []),
        ("塁", "るい", "bases / fort / rampart / walls / base (baseball)", ["ルイ"], ["とりで"]),
        ("塑", "そ", "model / molding", ["ソ"], ["でく"]),
        ("壁面", "へきめん", "wall surface", ["ヘキメン"], []),
    ],
    # Lesson 390
    [
        ("彫塑", "ちょうそ", "plastic arts / carving and modeling / sculpture", ["チョウソ"], []),
        ("塚", "つか", "mound / hillock / tumulus", ["チョウ"], ["つか", "-づか"]),
        ("墜", "つい", "crash / fall (down)", ["ツイ"], ["お.ちる", "お.つ"]),
        ("墜落", "ついらく", "falling / crashing (e.g. aircraft)", ["ツイラク"], []),
        ("神奈川", "かながわ", "Kanagawa", [], ["かながわ"]),
    ],
    # Lesson 391
    [
        ("墳", "ふん", "tomb / mound", ["フン"], []),
        ("古墳", "こふん", "ancient tomb / tumulus", ["コフン"], []),
        ("墾", "こん", "ground-breaking / open up farmland", ["コン"], []),
        ("開墾", "かいこん", "clearing land (for cultivation) / reclamation", ["カイコン"], []),
        ("団塊", "だんかい", "lump / mass / baby boom generation", ["ダンカイ"], []),
    ],
    # Lesson 392
    [
        ("壌", "じょう", "lot / earth / soil", ["ジョウ"], ["つち"]),
        ("平壌", "ピョンヤン", "Pyongyang (North Korea)", ["ヘイジョウ"], []),
        ("壱", "いち", "one (in documents)", ["イチ", "イツ"], ["ひとつ"]),
        ("奔", "ほん", "run / bustle", ["ホン"], ["はし.る"]),
        ("荒らす", "あらす", "to lay waste / devastate / damage / invade", ["コウ"], ["あら.す"]),
    ],
    # Lesson 393
    [
        ("奔放", "ほんぽう", "wild / uninhibited / extravagant / free-spirited", ["ホンポウ"], []),
        ("妃", "ひ", "queen / princess", ["ヒ"], ["きさき"]),
        ("妄", "もう", "delusion / unnecessarily / without authority", ["モウ", "ボウ"], ["みだ.りに"]),
        ("妄想", "もうそう", "wild idea / delusion", ["モウソウ"], []),
        ("驚異", "きょうい", "wonder / miracle / amazement / prodigy", ["キョウイ"], []),
    ],
    # Lesson 394
    [
        ("妊", "にん", "pregnancy", ["ニン", "ジン"], []),
        ("避妊", "ひにん", "contraception", ["ヒニン"], []),
        ("妥", "だ", "gentle / peace / depravity", ["ダ"], []),
        ("妥協", "だきょう", "compromise / giving in", ["ダキョウ"], []),
        ("妊婦", "にんぷ", "pregnant woman", ["ニンプ"], []),
    ],
    # Lesson 395
    [
        ("姫", "ひめ", "princess / young lady of noble birth", ["キ"], ["ひめ", "ひめ-"]),
        ("姻", "いん", "matrimony / marry", ["イン"], []),
        ("婚姻", "こんいん", "marriage / matrimony", ["コンイン"], []),
        ("娠", "しん", "with child / pregnancy", ["シン"], []),
        ("極楽", "ごくらく", "Sukhavati (Amitabha's Pure Land) / paradise", ["ゴクラク"], []),
    ],
    # Lesson 396
    [
        ("妊娠", "にんしん", "conception / pregnancy", ["ニンシン"], []),
        ("娯", "ご", "recreation / pleasure", ["ゴ"], []),
        ("娯楽", "ごらく", "pleasure / amusement / entertainment", ["ゴラク"], []),
        ("婆", "ばば", "old woman / grandma / wet nurse", ["バ"], ["ばば", "ばあ"]),
        ("老婆", "ろうば", "old woman", ["ロウバ"], []),
    ],
    # Lesson 397
    [
        ("媒", "ばい", "mediator / go-between", ["バイ"], ["なこうど"]),
        ("媒体", "ばいたい", "medium / media", ["バイタイ"], []),
        ("嫁", "よめ", "wife / bride / (one's) daughter-in-law", ["カ"], ["よめ", "とつ.ぐ"]),
        ("嫡", "ちゃく", "legitimate wife / direct descent (non-bastard)", ["チャク", "テキ"], []),
        ("尽力", "じんりょく", "efforts / exertion / assistance / good offices", ["ジンリョク"], []),
    ],
    # Lesson 398
    [
        ("嫡出", "ちゃくしゅつ", "legitimacy (of birth)", ["チャクシュツ"], []),
        ("孔", "こう", "cavity / hole / slit / very / great / exceedingly", ["コウ"], ["あな"]),
        ("孔子", "こうし", "Confucius", ["コウシ"], []),
        ("孤", "こ", "orphan / alone", ["コ"], []),
        ("腹筋", "ふっきん", "abdominal muscles / abs / sit-ups", ["フッキン"], []),
    ],
    # Lesson 399
    [
        ("孤児", "こじ", "orphan", ["コジ"], []),
        ("宰", "さい", "superintend / manager / rule", ["サイ"], []),
        ("主宰", "しゅさい", "supervision / chairmanship / presidency", ["シュサイ"], []),
        ("宵", "よい", "evening / early night hours", ["ショウ"], ["よい"]),
        ("映える", "はえる", "to shine / look attractive / look pretty", ["エイ"], ["は.える"]),
    ],
    # Lesson 400
    [
        ("寡", "か", "widow / minority / few", ["カ"], []),
        ("寡占", "かせん", "oligopoly", ["カセン"], []),
        ("審", "しん", "hearing / judge / trial", ["シン"], ["つまび.らか"]),
        ("審議", "しんぎ", "deliberation", ["シンギ"], []),
        ("審判", "しんぱん", "refereeing / trial / judgment / umpire / referee", ["シンパン"], []),
    ],
    # Lesson 401
    [
        ("尼", "あま", "nun", ["ニ"], ["あま"]),
        ("屯", "とん", "barracks / police station / camp / ton", ["トン"], ["たむろ"]),
        ("駐屯", "ちゅうとん", "stationing (of troops) / being stationed", ["チュウトン"], []),
        ("帆", "ほ", "sail", ["ハン"], ["ほ"]),
        ("亀裂", "きれつ", "crack / crevice / fissure / split / rift", ["キレツ"], []),
    ],
    # Lesson 402
    [
        ("帝", "てい", "sovereign / the emperor / god / creator", ["テイ"], ["みかど"]),
        ("帥", "すい", "commander / leading troops / governor", ["スイ"], []),
        ("元帥", "げんすい", "marshal / general of the army / admiral of the fleet", ["ゲンスイ"], []),
        ("幻", "まぼろし", "phantom / vision / dream / illusion / apparition", ["ゲン"], ["まぼろし"]),
        ("帝国", "ていこく", "empire / imperial", ["テイコク"], []),
    ],
    # Lesson 403
    [
        ("庶", "しょ", "commoner / all / bastard", ["ショ"], []),
        ("庶民", "しょみん", "common people / ordinary people / masses", ["ショミン"], []),
        ("庸", "よう", "commonplace / ordinary / employment", ["ヨウ"], []),
        ("凡庸", "ぼんよう", "mediocre / ordinary / commonplace / banal", ["ボンヨウ"], []),
        ("皇帝", "こうてい", "emperor", ["コウテイ"], []),
    ],
    # Lesson 404
    [
        ("廉", "れん", "bargain / reason / charge / suspicion / point", ["レン"], []),
        ("廉売", "れんばい", "bargain sale / selling at a discount", ["レンバイ"], []),
        ("廷", "てい", "courts / imperial court / government office", ["テイ"], []),
        ("法廷", "ほうてい", "courtroom", ["ホウテイ"], []),
        ("幻想", "げんそう", "fantasy / illusion / vision / dream", ["ゲンソウ"], []),
    ],
    # Lesson 405
    [
        ("弊", "へい", "abuse / evil / vice / breakage", ["ヘイ"], []),
        ("弊害", "へいがい", "evil / harmful effect / abuse / vice / bad influence", ["ヘイガイ"], []),
        ("弐", "に", "II / two / second", ["ニ", "ジ"], ["ふた.つ"]),
        ("弔う", "とむらう", "to mourn for / condole with / hold a memorial service", ["チョウ"], ["とむら.う"]),
        ("不吉", "ふきつ", "ominous / sinister / unlucky / inauspicious", ["フキツ"], []),
    ],
    # Lesson 406
    [
        ("弥", "や", "all the more / increasingly", ["ミ", "ビ"], ["いや", "や"]),
        ("弥生", "やよい", "third month of the lunar calendar / March / Yayoi", ["ヤヨイ"], []),
        ("弦", "げん", "bowstring / chord / hypotenuse", ["ゲン"], ["つる"]),
        ("弧", "こ", "arc / arch / bow", ["コ"], []),
        ("括弧", "かっこ", "parentheses / brackets", ["カッコ"], []),
    ],
    # Lesson 407
    [
        ("彰", "しょう", "patent / clear", ["ショウ"], []),
        ("表彰", "ひょうしょう", "public recognition / commendation", ["ヒョウショウ"], []),
        ("循", "じゅん", "sequential / fellow", ["ジュン"], []),
        ("循環", "じゅんかん", "circulation / rotation / cycle / loop", ["ジュンカン"], []),
        ("小豆", "あずき", "azuki bean / small red bean", ["ショウズ"], ["あずき"]),
    ],
    # Lesson 408
    [
        ("忌まわしい", "いまわしい", "unpleasant / abominable / detestable / unlucky", ["キ"], ["いま.わしい"]),
        ("忍ぶ", "しのぶ", "to conceal oneself / hide / bear / endure", ["ニン"], ["しの.ぶ", "しの.ばせる"]),
        ("恒", "こう", "constancy / always", ["コウ"], ["つね"]),
        ("恒例", "こうれい", "established practice / custom", ["コウレイ"], []),
        ("忍耐", "にんたい", "endurance / perseverance / patience", ["ニンタイ"], []),
    ],
    # Lesson 409
    [
        ("恭しい", "うやうやしい", "respectful / reverent", ["キョウ"], ["うやうや.しい"]),
        ("悠", "ゆう", "permanence / distant / long time / leisure", ["ユウ"], []),
        ("悠久", "ゆうきゅう", "eternity / perpetuity / permanence", ["ユウキュウ"], []),
        ("悦", "えつ", "ecstasy / joy / rapture", ["エツ"], ["よろこ.ぶ"]),
        ("逸脱", "いつだつ", "deviation / departure / aberration / omission", ["イツダツ"], []),
    ],
    # Lesson 410
    [
        ("満悦", "まんえつ", "great delight / rapture", ["マンエツ"], []),
        ("悼む", "いたむ", "to grieve over / mourn for", ["トウ"], ["いた.む"]),
        ("惰", "だ", "lazy / laziness", ["ダ"], []),
        ("惰性", "だせい", "inertia / momentum / force of habit", ["ダセイ"], []),
        ("伝票", "でんぴょう", "chit / sales slip / voucher", ["デンピョウ"], []),
    ],
    # Lesson 411
    [
        ("愁", "しゅう", "distress / grieve / lament / be anxious", ["シュウ"], ["うれ.える", "うれ.い"]),
        ("郷愁", "きょうしゅう", "nostalgia / homesickness", ["キョウシュウ"], []),
        ("慈", "じ", "mercy", ["ジ"], ["いつく.しむ"]),
        ("慈善", "じぜん", "charity / philanthropy", ["ジゼン"], []),
        ("勇敢", "ゆうかん", "brave / heroic / gallant", ["ユウカン"], []),
    ],
    # Lesson 412
    [
        ("憩い", "いこい", "rest / relaxation", ["ケイ"], ["いこ.い"]),
        ("憾", "かん", "remorse / regret / be sorry", ["カン"], ["うら.む"]),
        ("遺憾", "いかん", "regrettable / unsatisfactory / pitiful / deplorable", ["イカン"], []),
        ("懇", "こん", "sociable / kind / courteous / hospitable / cordial", ["コン"], ["ねんご.ろ"]),
        ("休憩", "きゅうけい", "rest / break / recess / intermission", ["キュウケイ"], []),
    ],
    # Lesson 413
    [
        ("懇談", "こんだん", "informal talk / familiar conversation / chat", ["コンダン"], []),
        ("扶", "ふ", "aid / help / assist", ["フ"], ["たす.ける"]),
        ("扶養", "ふよう", "support / maintenance", ["フヨウ"], []),
        ("抄", "しょう", "extract / selection / summary / copy", ["ショウ"], []),
        ("磁石", "じしゃく", "magnet / compass", ["ジシャク"], []),
    ],
    # Lesson 414
    [
        ("抄本", "しょうほん", "extract / abridged transcript / selection", ["ショウホン"], []),
        ("披", "ひ", "expose / open", ["ヒ"], []),
        ("披露", "ひろう", "announcement / presentation / showing", ["ヒロウ"], []),
        ("抵", "てい", "resist / reach / touch", ["テイ"], []),
        ("模倣", "もほう", "imitation / copying", ["モホウ"], []),
    ],
    # Lesson 415
    [
        ("抵抗", "ていこう", "electrical resistance / resistance / opposition", ["テイコウ"], []),
        ("抹", "まつ", "rub / paint / erase", ["マツ"], []),
        ("一抹", "いちまつ", "a touch of / a tinge of / a wreath (of smoke)", ["イチマツ"], []),
        ("抽", "ちゅう", "pluck / pull / extract / excel", ["チュウ"], ["ひき-"]),
        ("浮き彫り", "うきぼり", "relief / embossed carving / bringing to the fore", [], ["うきぼり"]),
    ],
    # Lesson 416
    [
        ("抽選", "ちゅうせん", "lottery / raffle / drawing (of lots)", ["チュウセン"], []),
        ("拐", "かい", "kidnap / falsify", ["カイ"], []),
        ("誘拐", "ゆうかい", "abduction / kidnapping / hijacking", ["ユウカイ"], []),
        ("拙", "せつ", "bungling / clumsy / unskillful", ["セツ"], ["つたな.い"]),
        ("成就", "じょうじゅ", "fulfillment / realization / completion / accomplishment", ["ジョウジュ"], []),
    ],
    # Lesson 417
    [
        ("拙速", "せっそく", "hasty / rough-and-ready", ["セッソク"], []),
        ("拷", "ごう", "torture / beat", ["ゴウ"], []),
        ("拷問", "ごうもん", "torture", ["ゴウモン"], []),
        ("搬", "はん", "conveyor / carry / transport", ["ハン"], []),
        ("口癖", "くちぐせ", "pet saying / favorite phrase / stock phrase", [], ["くちぐせ"]),
    ],
    # Lesson 418
    [
        ("運搬", "うんぱん", "transport / carriage", ["ウンパン"], []),
        ("搭", "とう", "board / load (a vehicle) / ride", ["トウ"], []),
        ("搭載", "とうさい", "loading (on board) / equipping", ["トウサイ"], []),
        ("搾", "さく", "squeeze", ["サク"], ["しぼ.る"]),
        ("網膜", "もうまく", "retina", ["モウマク"], []),
    ],
    # Lesson 419
    [
        ("搾取", "さくしゅ", "exploitation / squeezing / milking", ["サクシュ"], []),
        ("摂る", "とる", "to have (e.g. lunch) / take (e.g. vitamins)", ["セツ", "ショウ"], ["と.る"]),
        ("摂取", "せっしゅ", "intake / ingestion / absorption / adoption", ["セッシュ"], []),
        ("撤", "てつ", "remove / withdraw / disarm / dismantle", ["テツ"], []),
        ("撤廃", "てっぱい", "abolition / repeal / removal", ["テッパイ"], []),
    ],
    # Lesson 420
    [
        ("撤退", "てったい", "evacuation / withdrawal / revocation", ["テッタイ"], []),
        ("擁する", "ようする", "to have / possess / embrace / support", ["ヨウ"], ["よう.する"]),
        ("擬", "ぎ", "mimic / aim (a gun) at / nominate / imitate", ["ギ"], ["まが.い", "もど.き"]),
        ("模擬", "もぎ", "imitation / sham / mock / simulation", ["モギ"], []),
        ("褒美", "ほうび", "reward / prize", ["ホウビ"], []),
    ],
    # Lesson 421
    [
        ("敏", "びん", "cleverness / agile / alert", ["ビン"], ["さと.い"]),
        ("敏感", "びんかん", "sensitive / alert / susceptible", ["ビンカン"], []),
        ("斗", "と", "Big Dipper / ten sho (vol) / sake dipper", ["ト", "トウ"], []),
        ("斤", "きん", "axe / 1.32 lb / catty", ["キン"], []),
        ("化ける", "ばける", "to take the form of (esp. in ref. to a spirit, fox, etc.) / transform", ["カ", "ケ"], ["ば.ける", "ば.かす"]),
    ],
    # Lesson 422
    [
        ("斥", "せき", "reject / retreat / recede / withdraw / repel", ["セキ"], ["しりぞ.ける"]),
        ("排斥", "はいせき", "rejection / expulsion / boycott / ostracism", ["ハイセキ"], []),
        ("旋", "せん", "rotation / go around", ["セン"], []),
        ("旋風", "せんぷう", "whirlwind / sensation / commotion", ["センプウ"], []),
        ("群がる", "むらがる", "to swarm / gather", ["グン"], ["むら.がる"]),
    ],
    # Lesson 423
    [
        ("旺", "おう", "flourishing / successful / beautiful / vigorous", ["オウ"], []),
        ("旺盛", "おうせい", "lively / vigorous / energetic / healthy", ["オウセイ"], []),
        ("昆", "こん", "descendants / elder brother / insect", ["コン"], []),
        ("昆虫", "こんちゅう", "insect / bug", ["コンチュウ"], []),
        ("善し悪し", "よしあし", "good or bad / merits or demerits / quality / suitability", [], ["よしあし"]),
    ],
    # Lesson 424
    [
        ("晶", "しょう", "sparkle / clear / crystal", ["ショウ"], []),
        ("液晶", "えきしょう", "liquid crystal", ["エキショウ"], []),
        ("暁", "あかつき", "dawn / daybreak / in the event of", ["ギョウ", "キョウ"], ["あかつき", "さと.る"]),
        ("曹", "そう", "office / official / comrade / fellow", ["ソウ", "ゾウ"], []),
        ("悔やむ", "くやむ", "to mourn / lament / be sorry / regret / repent", ["カイ"], ["くや.む", "くや.しい"]),
    ],
    # Lesson 425
    [
        ("法曹", "ほうそう", "legal profession / judicial circles", ["ホウソウ"], []),
        ("朕", "ちん", "majestic plural / imperial we", ["チン"], []),
        ("朱", "しゅ", "vermilion / cinnabar / scarlet / red / bloody", ["シュ"], ["あけ"]),
        ("朽ちる", "くちる", "to rot / decay / remain in seclusion", ["キュウ"], ["く.ちる"]),
        ("歓喜", "かんき", "delight / great joy", ["カンキ"], []),
    ],
    # Lesson 426
    [
        ("老朽", "ろうきゅう", "superannuation / decrepitude / wearing out", ["ロウキュウ"], []),
        ("析", "せき", "chop / divide / tear / analyze", ["セキ"], []),
        ("分析", "ぶんせき", "analysis", ["ブンセキ"], []),
        ("某", "ぼう", "so-and-so / one / a certain / that person", ["ボウ"], ["それがし", "なにがし"]),
        ("楽観", "らっかん", "optimism / taking an optimistic view", ["ラッカン"], []),
    ],
    # Lesson 427
    [
        ("柳", "やなぎ", "willow", ["リュウ"], ["やなぎ"]),
        ("栓", "せん", "plug / cork / stopper / bung", ["セン"], []),
        ("栽", "さい", "plantation / planting", ["サイ"], []),
        ("栽培", "さいばい", "cultivation", ["サイバイ"], []),
        ("抹茶", "まっちゃ", "matcha / powdered green tea", ["マッチャ"], []),
    ],
    # Lesson 428
    [
        ("桃", "もも", "peach", ["トウ"], ["もも"]),
        ("桑", "くわ", "mulberry", ["ソウ"], ["くわ"]),
        ("棋", "き", "chess piece / Japanese chess / shogi", ["キ"], []),
        ("将棋", "しょうぎ", "shogi / Japanese chess", ["ショウギ"], []),
        ("伝言", "でんごん", "verbal message / rumor / word", ["デンゴン"], []),
    ],
    # Lesson 429
    [
        ("棺", "ひつぎ", "coffin / casket", ["カン"], ["ひつぎ"]),
        ("椎", "しい", "chinquapin / mallet / spine", ["ツイ", "スイ"], ["しい", "う.つ"]),
        ("椎間板", "ついかんばん", "intervertebral disk", ["ツイカンバン"], []),
        ("楼", "ろう", "watchtower / lookout / high building", ["ロウ"], ["たかどの"]),
        ("却下", "きゃっか", "rejection / dismissal / turning down", ["キャッカ"], []),
    ],
    # Lesson 430
    [
        ("楼閣", "ろうかく", "palace / multistoried building / tower", ["ロウカク"], []),
        ("槽", "そう", "vat / tub / tank", ["ソウ"], ["ふね"]),
        ("水槽", "すいそう", "water tank / cistern / fish tank / aquarium", ["スイソウ"], []),
        ("款", "かん", "goodwill / article / section / friendship / collusion", ["カン"], []),
        ("約款", "やっかん", "agreement / stipulation / article / clause", ["ヤッカン"], []),
    ],
    # Lesson 431
    [
        ("借款", "しゃっかん", "loan / credit", ["シャッカン"], []),
        ("殉", "じゅん", "martyrdom / follow by resigning", ["ジュン"], []),
        ("殉教", "じゅんきょう", "martyrdom", ["ジュンキョウ"], []),
        ("江", "え", "creek / inlet / bay", ["コウ"], ["え"]),
        ("偽り", "いつわり", "lie / falsehood / fiction / fabrication", ["ギ"], ["いつわ.り"]),
    ],
    # Lesson 432
    [
        ("汰", "た", "luxury / select", ["タ", "タイ"], ["よな.げる"]),
        ("沙", "さ", "sand", ["サ", "シャ"], ["すな"]),
        ("沙汰", "さた", "affair / state / news / tidiness / instructions / order", ["サタ"], []),
        ("泌", "ひつ", "ooze / flow / soak in / penetrate / secrete", ["ヒツ", "ヒ"], []),
        ("遊戯", "ゆうぎ", "game / play / sports", ["ユウギ"], []),
    ],
    # Lesson 433
    [
        ("分泌", "ぶんぴつ", "secretion", ["ブンピツ", "ブンピ"], []),
        ("泰", "たい", "peaceful / calm / peace / easy / Thailand / extreme / excessive", ["タイ"], []),
        ("洞", "ほら", "den / cave / excavation", ["ドウ"], ["ほら"]),
        ("洪", "こう", "deluge / flood / vast", ["コウ"], []),
        ("氷河", "ひょうが", "glacier", ["ヒョウガ"], []),
    ],
    # Lesson 434
    [
        ("洪水", "こうずい", "flood / inundation", ["コウズイ"], []),
        ("浄", "じょう", "clean / purify / cleanse / exorcise / Manchu Dynasty", ["ジョウ", "セイ"], ["きよ.める", "きよ.い"]),
        ("浄化", "じょうか", "purification / cleanup / purge", ["ジョウカ"], []),
        ("浦", "うら", "bay / creek / inlet / gulf / beach / seacoast", ["ホ"], ["うら"]),
        ("略奪", "りゃくだつ", "pillage / plunder / looting / robbery", ["リャクダツ"], []),
    ],
    # Lesson 435
    [
        ("浪", "ろう", "wandering / waves / billows", ["ロウ"], []),
        ("涯", "がい", "horizon / shore / limit / bound", ["ガイ"], ["はて"]),
        ("生涯", "しょうがい", "one's life / a lifetime / career", ["ショウガイ"], []),
        ("淑", "しゅく", "graceful / gentle / pure", ["シュク"], ["しと.やか"]),
        ("浪人", "ろうにん", "ronin (masterless samurai) / student waiting for another chance to enter university", ["ロウニン"], []),
    ],
    # Lesson 436
    [
        ("淑女", "しゅくじょ", "lady", ["シュクジョ"], []),
        ("渉", "しょう", "ford / go cross / ferry / import / involve", ["ショウ"], ["わた.る"]),
        ("交渉", "こうしょう", "negotiations / discussions / connection", ["コウショウ"], []),
        ("渓", "けい", "mountain stream / valley", ["ケイ"], ["たに", "たにがわ"]),
        ("田畑", "たはた", "fields (rice paddies and other fields)", [], ["たはた"]),
    ],
    # Lesson 437
    [
        ("渓谷", "けいこく", "valley / ravine / canyon", ["ケイコク"], []),
        ("漆", "うるし", "lacquer / varnish / seven", ["シツ"], ["うるし"]),
        ("漠", "ばく", "vague / obscure / desert / wide", ["バク"], []),
        ("砂漠", "さばく", "desert", ["サバク"], []),
        ("感嘆", "かんたん", "admiration / wonder", ["カンタン"], []),
    ],
    # Lesson 438
    [
        ("滴", "しずく", "drip / drop", ["テキ"], ["しずく", "したた.る"]),
        ("漸進", "ぜんしん", "gradual progress / steady advance", ["ゼンシン"], []),
        ("濫", "らん", "excessive / overflow / spread out", ["ラン"], ["みだ.りに", "みだ.りがましい"]),
        ("濫造", "らんぞう", "overproduction / careless manufacture", ["ランゾウ"], []),
        ("漸く", "ようやく", "finally / at last / barely / narrowly / gradually", ["ゼン"], ["ようや.く"]),
    ],
    # Lesson 439
    [
        ("炉", "ろ", "hearth / furnace / kiln / reactor", ["ロ"], ["いろり"]),
        ("原子炉", "げんしろ", "nuclear reactor", ["ゲンシロ"], []),
        ("烈", "れつ", "ardent / violent / vehement / furious / severe / extreme", ["レツ"], ["はげ.しい"]),
        ("強烈", "きょうれつ", "strong / intense / severe", ["キョウレッ"], []),
        ("卓球", "たっきゅう", "table tennis / ping-pong", ["タッキュウ"], []),
    ],
    # Lesson 440
    [
        ("煩い", "うるさい", "noisy / loud / annoying / troublesome / fussy", ["ハン", "ボン"], ["わずら.わしい", "うるさ.い"]),
        ("爵", "しゃく", "baron / peerage / court rank", ["シャク"], []),
        ("伯爵", "はくしゃく", "count / earl", ["ハクシャク"], []),
        ("牲", "せい", "animal sacrifice / offering", ["セイ"], []),
        ("傘下", "さんか", "affiliated with / under the umbrella (wing) of", ["サンカ"], []),
    ],
    # Lesson 441
    [
        ("犠", "ぎ", "sacrifice", ["ギ"], ["いけにえ"]),
        ("犠牲者", "ぎせいしゃ", "victim / prey", ["ギセイシャ"], []),
        ("狩り", "かり", "hunting", ["シュ"], ["か.り"]),
        ("猟", "りょう", "game-hunting / shooting / game / bag", ["リョウ", "レフ"], ["かり"]),
        ("狩猟", "しゅりょう", "hunting", ["シュリョウ"], []),
    ],
    # Lesson 442
    [
        ("猶", "ゆう", "furthermore / still / yet", ["ユウ", "ユ"], ["なお"]),
        ("執行猶予", "しっこうゆうよ", "stay of execution / suspended sentence", ["シッコウユウヨ"], []),
        ("珠", "しゅ", "pearl / gem / jewel", ["シュ"], ["たま"]),
        ("真珠", "しんじゅ", "pearl", ["シンジュ"], []),
        ("即決", "そっけつ", "immediate decision / prompt decision / snap judgment", ["ソッケツ"], []),
    ],
    # Lesson 443
    [
        ("瑠", "る", "lapis lazuli", ["ル", "リュウ"], []),
        ("璃", "り", "glassy / lapis lazuli", ["リ"], []),
        ("浄瑠璃", "じょうるり", "joruri (traditional Japanese narrative music)", ["ジョウルリ"], []),
        ("璽", "じ", "emperor's seal", ["ジ"], []),
        ("万博", "ばんぱく", "world's fair / international exposition", ["バンパク"], []),
    ],
    # Lesson 444
    [
        ("畔", "はん", "paddy-ridge / levee", ["ハン"], ["あぜ", "くろ", "ほとり"]),
        ("湖畔", "こはん", "lake shore", ["コハン"], []),
        ("畝", "うね", "furrow / thirty tsubo / ridge / rib", ["ボウ", "ホ", "モ"], ["せ", "うね"]),
        ("疫", "えき", "epidemic", ["エキ", "ヤク"], []),
        ("研ぐ", "とぐ", "to sharpen / hone / whet / grind / wash (rice)", ["ケン"], ["と.ぐ"]),
    ],
    # Lesson 445
    [
        ("免疫", "めんえき", "immunity / immunization", ["メンエキ"], []),
        ("サル痘", "サルとう", "mpox / monkeypox", ["トウ"], []),
        ("種痘", "しゅとう", "vaccination (smallpox) / inoculation", ["シュトウ"], []),
        ("痢", "り", "diarrhea", ["リ"], []),
        ("手拭い", "てぬぐい", "hand towel", [], ["てぬぐい"]),
    ],
    # Lesson 446
    [
        ("下痢", "げり", "diarrhea", ["ゲリ"], []),
        ("癒", "ゆ", "healing / cure / quench (thirst) / wreak", ["ユ"], ["い.える", "いや.す"]),
        ("癒着", "ゆちゃく", "adhesion / collusion", ["ユチャク"], []),
        ("盲", "もう", "blind / blind man / ignoramus", ["モウ"], ["めくら"]),
        ("癒す", "いやす", "to heal / cure / satisfy (e.g. hunger, thirst)", ["ユ"], ["いや.す"]),
    ],
    # Lesson 447
    [
        ("睦む", "むつむ", "to be intimate with / be friendly with", ["ボク", "モク"], ["むつ.む", "むつ.まじい"]),
        ("瞭", "りょう", "clear", ["リョウ"], ["あきらか"]),
        ("明瞭", "めいりょう", "clear / plain / distinct / obvious / evident / articulate", ["メイリョウ"], []),
        ("矯", "きょう", "rectify / straighten / correct / reform / cure", ["キョウ"], ["た.める"]),
        ("漫才", "まんざい", "manzai / comic dialogue / stand-up comedy", ["マンザイ"], []),
    ],
    # Lesson 448
    [
        ("矯正", "きょうせい", "correction (of fault, defect, flaw, etc.)", ["キョウセイ"], []),
        ("硝", "しょう", "nitrate / saltpeter", ["ショウ"], []),
        ("硝酸", "しょうさん", "nitric acid", ["ショウサン"], []),
        ("硫", "りゅう", "sulphur", ["リュウ"], []),
        ("発泡", "はっぽう", "foaming / effervescent / sparkling", ["ハッポウ"], []),
    ],
    # Lesson 449
    [
        ("硫黄", "いおう", "sulfur / sulphur", ["リュウオウ"], ["いおう"]),
        ("礁", "しょう", "reef / sunken rock", ["ショウ"], []),
        ("暗礁", "あんしょう", "reef / sunken rock / unforeseen difficulty", ["アンショウ"], []),
        ("祉", "し", "welfare / happiness", ["シ"], []),
        ("挿絵", "さしえ", "illustration (e.g. book)", [], ["さしえ"]),
    ],
    # Lesson 450
    [
        ("福祉", "ふくし", "welfare / well-being / social welfare", ["フクシ"], []),
        ("祥", "しょう", "auspicious / happiness / blessedness / good omen", ["ショウ"], ["さいわ.い", "きざ.し"]),
        ("不祥事", "ふしょうじ", "scandal / deplorable event", ["フショウジ"], []),
        ("禍", "か", "calamity / misfortune / evil / curse", ["カ"], ["わざわい"]),
        ("心細い", "こころぼそい", "helpless / forlorn / hopeless / unpromising", [], ["こころぼそ.い"]),
    ],
    # Lesson 451
    [
        ("惨禍", "さんか", "calamity / disaster / tragedy", ["サンカ"], []),
        ("租", "そ", "tariff / crop tax / borrowing", ["ソ"], []),
        ("租税", "そぜい", "taxes / taxation", ["ソゼイ"], []),
        ("秩", "ちつ", "regularity / salary / order", ["チツ"], []),
        ("砂利", "じゃり", "gravel / ballast / pebbles", ["ジャリ"], []),
    ],
    # Lesson 452
    [
        ("秩序", "ちつじょ", "order / discipline / regularity / system", ["チツジョ"], []),
        ("穫", "かく", "harvest / reap", ["カク"], []),
        ("収穫", "しゅうかく", "harvest / crop / ingathering / gain", ["シュウカク"], []),
        ("窃", "せつ", "stealth / steal / secret / private / hushed", ["セツ"], ["ぬす.む", "ひそ.か"]),
        ("発砲", "はっぽう", "firing (a gun) / shooting / discharge", ["ハッポウ"], []),
    ],
    # Lesson 453
    [
        ("窃盗", "せっとう", "theft / stealing / larceny", ["セットウ"], []),
        ("窒", "ちつ", "plug up / obstruct", ["チツ"], []),
        ("窒素", "ちっそ", "nitrogen (N)", ["チッソ"], []),
        ("窯", "かま", "kiln / oven / furnace", ["ヨウ"], ["かま"]),
        ("草履", "ぞうり", "zori (traditional Japanese footwear)", ["ゾウリ"], []),
    ],
    # Lesson 454
    [
        ("竜", "りゅう", "dragon / imperial", ["リュウ", "リョウ", "ロウ"], ["たつ"]),
        ("篤と", "とくと", "carefully / thoroughly / deliberately", ["トク"], ["とく.と"]),
        ("危篤", "きとく", "critical condition (of a patient)", ["キトク"], []),
        ("簿", "ぼ", "register / record book", ["ボ"], []),
        ("恐竜", "きょうりゅう", "dinosaur", ["キョウリュウ"], []),
    ],
    # Lesson 455
    [
        ("名簿", "めいぼ", "register of names / list of names / roll", ["メイボ"], []),
        ("粗い", "あらい", "coarse / rough", ["ソ"], ["あら.い"]),
        ("粛", "しゅく", "solemn / quietly / softly", ["シュク", "スク"], ["つつし.む"]),
        ("自粛", "じしゅく", "self-restraint / voluntary restraint", ["ジシュク"], []),
        ("粗末", "そまつ", "crude / rough / plain / humble / shabby", ["ソマツ"], []),
    ],
    # Lesson 456
    [
        ("糾", "きゅう", "twist / ask / investigate / verify", ["キュウ"], ["ただ.す"]),
        ("紛糾", "ふんきゅう", "complication / confusion / disorder", ["フンキュウ"], []),
        ("紋", "もん", "family crest / figures", ["モン"], []),
        ("紡ぐ", "つむぐ", "to spin (yarn/thread)", ["ボウ"], ["つむ.ぐ"]),
        ("舞踏", "ぶとう", "dancing / ball", ["ブトウ"], []),
    ],
    # Lesson 457
    [
        ("累", "るい", "accumulate / involvement / trouble / tie up", ["ルイ"], []),
        ("累積", "るいせき", "accumulation", ["ルイセキ"], []),
        ("維", "い", "fiber / tie / rope", ["イ"], []),
        ("維持", "いじ", "maintenance / preservation / improvement", ["イジ"], []),
        ("仰天", "ぎょうてん", "being amazed / being horrified / astonishment", ["ギョウテン"], []),
    ],
    # Lesson 458
    [
        ("緯", "い", "horizontal / woof / left & right / latitude", ["イ"], ["よこいと", "ぬき"]),
        ("経緯", "けいい", "details / particulars / sequence of events", ["ケイイ"], []),
        ("繕", "ぜん", "darn / repair / mend / trim / tidy up / adjust", ["ゼン"], ["つくろ.う"]),
        ("修繕", "しゅうぜん", "repair / mending / overhaul", ["シュウゼン"], []),
        ("三味", "さんみ", "three tastes / absorption / samadhi", ["サンミ"], []),
    ],
    # Lesson 459
    [
        ("繭", "まゆ", "cocoon", ["ケン"], ["まゆ"]),
        ("罷", "ひ", "quit / stop / leave / withdraw / go", ["ヒ"], ["まか.り-", "や.める"]),
        ("罷免", "ひめん", "dismissal / discharge", ["ヒメン"], []),
        ("羅", "ら", "gauze / thin silk / Rome / arrange / spread out", ["ラ"], ["うすもの"]),
        ("心拍", "しんぱく", "heartbeat / heart rate", ["シンパク"], []),
    ],
    # Lesson 460
    [
        ("修羅場", "しゅらば", "scene of carnage / fight scene / crisis", ["シュラバ"], []),
        ("翁", "おう", "venerable old man", ["オウ"], ["おきな"]),
        ("耗", "もう", "decrease", ["モウ", "コウ"], []),
        ("消耗", "しょうもう", "exhaustion / consumption", ["ショウモウ"], []),
        ("凝縮", "ぎょうしゅく", "condensation / concentration", ["ギョウシュク"], []),
    ],
    # Lesson 461
    [
        ("聴", "ちょう", "listen / headstrong / naughty / careful inquiry", ["チョウ", "テイ"], ["き.く", "ゆる.す"]),
        ("聴取", "ちょうしゅ", "listening / hearing / audition / radio reception", ["チョウシュ"], []),
        ("肖", "しょう", "resemblance", ["ショウ"], ["あやか.る"]),
        ("肖像", "しょうぞう", "portrait / likeness / picture", ["ショウゾウ"], []),
        ("傍聴", "ぼうちょう", "hearing / attendance / auditing", ["ボウチョウ"], []),
    ],
    # Lesson 462
    [
        ("肢", "し", "limb / arms & legs", ["シ"], []),
        ("選択肢", "せんたくし", "choices / alternatives / options", ["センタクシ"], []),
        ("肪", "ぼう", "obese / fat", ["ボウ"], []),
        ("脂肪", "しぼう", "fat / grease / blubber / lard / suet", ["シボウ"], []),
        ("飽和", "ほうわ", "saturation", ["ホウワ"], []),
    ],
    # Lesson 463
    [
        ("胆", "きも", "liver / innards / courage / pluck", ["タン"], ["きも"]),
        ("大胆", "だいたん", "bold / daring / audacious", ["ダイタン"], []),
        ("胎", "たい", "womb / uterus", ["タイ"], []),
        ("胎児", "たいじ", "fetus / embryo", ["タイジ"], []),
        ("度胸", "どきょう", "courage / bravery / nerve / pluck / guts", ["ドキョウ"], []),
    ],
    # Lesson 464
    [
        ("胞", "ほう", "placenta / sac / sheath", ["ホウ"], []),
        ("細胞", "さいぼう", "cell (biology)", ["サイボウ"], []),
        ("舶", "はく", "liner / ship", ["ハク"], []),
        ("船舶", "せんぱく", "vessel / ship / shipping / seacraft", ["センパク"], []),
        ("共働き", "ともばたらき", "dual income / both spouses working", [], ["ともばたらき"]),
    ],
    # Lesson 465
    [
        ("艇", "てい", "rowboat / small boat", ["テイ"], []),
        ("艦艇", "かんてい", "warships / naval vessels", ["カンテイ"], []),
        ("芋", "いも", "potato", ["ウ"], ["いも"]),
        ("芳しい", "かんばしい", "sweet / fragrant / aromatic / favorable", ["ホウ"], ["かんば.しい"]),
        ("末尾", "まつび", "end", ["マツビ"], []),
    ],
    # Lesson 466
    [
        ("菊", "きく", "chrysanthemum", ["キク"], []),
        ("薪", "まき", "firewood / kindling / fuel", ["シン"], ["たきぎ", "まき"]),
        ("薫", "くん", "send forth fragrance / fragrant / be scented", ["クン"], ["かお.る"]),
        ("藍", "あい", "indigo", ["ラン"], ["あい"]),
        ("菜の花", "なのはな", "rapeseed blossoms / canola flower", [], ["なのはな"]),
    ],
    # Lesson 467
    [
        ("藤", "ふじ", "wisteria", ["トウ"], ["ふじ"]),
        ("藩", "はん", "clan / enclosure", ["ハン"], []),
        ("藻", "も", "algae / seaweed / duckweed", ["ソウ"], ["も"]),
        ("虐げる", "しいたげる", "to oppress / tyrannize / persecute / treat cruelly", ["ギャク"], ["しいた.げる"]),
        ("虐待", "ぎゃくたい", "abuse / ill-treatment / maltreatment / cruelty", ["ギャクタイ"], []),
    ],
    # Lesson 468
    [
        ("虞", "おそれ", "fear / anxiety / concern / uneasiness", ["グ"], ["おそれ"]),
        ("虹", "にじ", "rainbow", ["コウ"], ["にじ"]),
        ("蚊", "か", "mosquito", ["ブン"], ["か"]),
        ("蛍", "ほたる", "lightning-bug / firefly", ["ケイ"], ["ほたる"]),
        ("佐藤", "さとう", "Sato (surname)", [], ["さとう"]),
    ],
    # Lesson 469
    [
        ("蛮", "ばん", "barbarian", ["バン"], ["えびす"]),
        ("野蛮", "やばん", "savage / barbarous / barbaric / uncivilized", ["ヤバン"], []),
        ("融", "ゆう", "dissolve / melt", ["ユウ"], ["と.ける", "と.かす"]),
        ("金融", "きんゆう", "financing / credit transacting / loaning of money / banking", ["キンユウ"], []),
        ("蛍光", "けいこう", "fluorescence", ["ケイコウ"], []),
    ],
    # Lesson 470
    [
        ("衷", "ちゅう", "inmost / heart / mind / inside", ["チュウ"], []),
        ("折衷", "せっちゅう", "compromise / cross / blending / eclecticism", ["セッチュウ"], []),
        ("裕", "ゆう", "abundant / rich / fertile", ["ユウ"], []),
        ("余裕", "よゆう", "surplus / margin / leeway / room / time", ["ヨユウ"], []),
        ("近藤", "こんどう", "Kondo (surname)", [], ["こんどう"]),
    ],
    # Lesson 471
    [
        ("褐", "かつ", "brown / woolly kimono", ["カツ"], []),
        ("褐色", "かっしょく", "brown / dark brown", ["カッショク"], []),
        ("覇", "は", "hegemony / supremacy / leadership / champion", ["ハ", "ハク"], []),
        ("連覇", "れんぱ", "consecutive championships / winning consecutively", ["レンパ"], []),
        ("融通", "ゆうずう", "flexibility / adaptability / lending (money) / accommodation", ["ユウズウ"], []),
    ],
    # Lesson 472
    [
        ("訟", "しょう", "sue / accuse", ["ショウ"], []),
        ("訴訟", "そしょう", "litigation / lawsuit", ["ソショウ"], []),
        ("詐", "さ", "lie / falsehood / deceive / pretend", ["サ"], ["いつわ.る"]),
        ("詐欺", "さぎ", "fraud / swindle / graft / cheating / scam", ["サギ"], []),
        ("片っ端", "かたっぱし", "one end / every single one / one after another", [], ["かたっぱし"]),
    ],
    # Lesson 473
    [
        ("詔", "みことのり", "imperial edict", ["ショウ"], ["みことのり"]),
        ("詠む", "よむ", "to compose (a Japanese poem) / recite", ["エイ"], ["よ.む"]),
        ("諭す", "さとす", "to admonish / persuade / counsel / warn", ["ユ"], ["さと.す"]),
        ("諮る", "はかる", "to consult with / confer", ["シ"], ["はか.る"]),
        ("諮問", "しもん", "consultation / inquiry", ["シモン"], []),
    ],
    # Lesson 474
    [
        ("謀", "はかりごと", "plan / plot / scheme / stratagem", ["ボウ", "ム"], ["はか.る", "はかりごと"]),
        ("謁", "えつ", "audience / audience (with king)", ["エツ"], []),
        ("謄", "とう", "mimeograph / copy", ["トウ"], []),
        ("謄本", "とうほん", "certified copy / transcript / duplicate", ["トウホン"], []),
        ("参謀", "さんぼう", "staff officer / participation in planning", ["サンボウ"], []),
    ],
    # Lesson 475
    [
        ("謹んで", "つつしんで", "respectfully / humbly / reverently", ["キン"], ["つつし.んで"]),
        ("謹慎", "きんしん", "penitence / self-restraint / house arrest", ["キンシン"], []),
        ("貞", "てい", "upright / chastity / constancy / righteousness", ["テイ", "ジョウ"], ["さだ"]),
        ("賊", "ぞく", "burglar / rebel / traitor / robber", ["ゾク"], []),
        ("教諭", "きょうゆ", "(licensed) teacher", ["キョウユ"], []),
    ],
    # Lesson 476
    [
        ("すい賓", "すいひん", "honored guest", ["ヒン"], []),
        ("迎賓館", "げいひんかん", "state guesthouse / reception hall for state guests", ["ゲイヒンカン"], []),
        ("賜る", "たまわる", "to grant / bestow / confer / be given", ["シ"], ["たまわ.る", "たま.う"]),
        ("賜杯", "しはい", "trophy given by the Emperor", ["シハイ"], []),
        ("狭間", "はざま", "interval / space / interstice / threshold / valley", ["キョウ"], ["はざま"]),
    ],
    # Lesson 477
    [
        ("賄", "わいろ", "bribe", ["ワイ"], ["まかな.う"]),
        ("賠償", "ばいしょう", "reparations / indemnity / compensation", ["バイショウ"], []),
        ("賦", "ふ", "levy / ode / prose / poem / tribute / installment", ["フ", "ブ"], []),
        ("割賦", "かっぷ", "allotment / quota / installment (payment)", ["カップ"], []),
        ("凸凹", "でこぼこ", "unevenness / roughness / ruggedness", ["オウトツ"], ["でこぼこ"]),
    ],
    # Lesson 478
    [
        ("赦", "しゃ", "pardon / forgiveness", ["シャ"], ["ゆる.す"]),
        ("恩赦", "おんしゃ", "amnesty / general pardon", ["オンシャ"], []),
        ("践", "せん", "tread / step on / trample / practice", ["セン"], ["ふ.む"]),
        ("実践", "じっせん", "practice / putting into practice", ["ジッセン"], []),
        ("固執", "こしつ", "adherence / persistence / obstinacy", ["コシツ"], []),
    ],
    # Lesson 479
    [
        ("軌", "き", "rut / wheel / track / model / way of doing", ["キ"], []),
        ("軌道", "きどう", "orbit / trajectory / railroad track", ["キドウ"], []),
        ("較", "かく", "contrast / compare", ["カク", "コウ"], ["くら.べる"]),
        ("比較", "ひかく", "comparison", ["ヒカク"], []),
        ("鈍る", "にぶる", "to become blunt / grow dull / weaken", ["ドン"], ["にぶ.る"]),
    ],
    # Lesson 480
    [
        ("轄", "かつ", "control / wedge", ["カツ"], ["くさび"]),
        ("管轄", "かんかつ", "jurisdiction / control", ["カンカツ"], []),
        ("迅", "じん", "swift / fast", ["ジン"], ["はや.い"]),
        ("迅速", "じんそく", "quick / fast / rapid / swift / prompt", ["ジンソク"], []),
        ("追悼", "ついとう", "mourning / memorial", ["ツイトウ"], []),
    ],
    # Lesson 481
    [
        ("迭", "てつ", "transfer / alternation", ["テツ"], []),
        ("更迭", "こうてつ", "change / shake-up / reshuffle / replacement", ["コウテツ"], []),
        ("逐", "ちく", "pursue / drive away / chase / accomplish", ["チク"], []),
        ("駆逐艦", "くちくかん", "destroyer (ship)", ["クチクカン"], []),
        ("因縁", "いんねん", "fate / destiny / connection / origin", ["インネン"], []),
    ],
    # Lesson 482
    [
        ("逓", "てい", "relay / in turn / sending", ["テイ"], ["かわ.る", "たがいに"]),
        ("逓信", "ていしん", "communications (post & telecommunications)", ["テイシン"], []),
        ("逝", "せい", "departed / die", ["セイ"], ["ゆ.く", "い.く"]),
        ("逝去", "せいきょ", "death / passing", ["セイキョ"], []),
        ("由緒", "ゆいしょ", "history / pedigree / lineage", ["ユイショ"], []),
    ],
    # Lesson 483
    [
        ("遵", "じゅん", "abide by / follow / obey / learn", ["ジュン"], []),
        ("遵守", "じゅんしゅ", "observance / obeying / abiding by", ["ジュンシュ"], []),
        ("遷", "せん", "transition / move / change", ["セン"], ["うつ.る", "うつ.す"]),
        ("変遷", "へんせん", "change / transition / vicissitudes", ["ヘンセン"], []),
        ("面目", "めんぼく", "face / honor / dignity / reputation / appearance", ["メンボク", "メンモク"], []),
    ],
    # Lesson 484
    [
        ("還", "かん", "send back / return", ["カン"], ["かえ.る"]),
        ("返還", "へんかん", "return / restoration", ["ヘンカン"], []),
        ("那", "な", "what?", ["ナ", "ダ"], ["なに", "なんぞ"]),
        ("旦那", "だんな", "master (of a house/shop) / husband / sir", ["ダンナ"], []),
        ("伴奏", "ばんそう", "accompaniment (musical)", ["バンソウ"], []),
    ],
    # Lesson 485
    [
        ("邦", "ほう", "home country / country / Japan", ["ホウ"], ["くに"]),
        ("連邦", "れんぽう", "commonwealth / federation of states / union", ["レンポウ"], []),
        ("郎", "ろう", "son / counter for sons", ["ロウ", "リョウ"], ["おとこ"]),
        ("新郎", "しんろう", "bridegroom", ["シンロウ"], []),
        ("殿様", "とのさま", "feudal lord", [], ["とのさま"]),
    ],
    # Lesson 486
    [
        ("郭", "かく", "enclosure / quarters / fortification / red-light district", ["カク"], ["くるわ"]),
        ("外郭団体", "がいかくだんたい", "auxiliary organization / affiliated agency", ["ガイカクダンタイ"], []),
        ("酢", "す", "vinegar / sour / acid / tart", ["サク"], ["す"]),
        ("酪", "らく", "dairy products / whey / broth / fruit juice", ["ラク"], []),
        ("頂", "いただき", "crown (of head) / summit (of mountain) / spire", ["チョウ"], ["いただ.く", "いただき"]),
    ],
    # Lesson 487
    [
        ("酪農", "らくのう", "dairy farming", ["ラクノウ"], []),
        ("酬", "しゅう", "repay / reward / retribution", ["シュウ", "シュ", "トウ"], ["むく.いる"]),
        ("報酬", "ほうしゅう", "remuneration / recompense / reward / toll", ["ホウシュウ"], []),
        ("酵", "こう", "ferment", ["コウ"], []),
        ("爽快", "そうかい", "refreshing / exhilarating / invigorating", ["ソウカイ"], []),
    ],
    # Lesson 488
    [
        ("酵素", "こうそ", "enzyme", ["コウソ"], []),
        ("醸す", "かもす", "to brew / cause / give rise to", ["ジョウ"], ["かも.す"]),
        ("醸成", "じょうせい", "brew / foment / engender / foster", ["ジョウセイ"], []),
        ("采", "さい", "dice / form / appearance / take / authority", ["サイ"], ["と.る", "いろどり"]),
        ("宮崎", "みやざき", "Miyazaki", [], ["みやざき"]),
    ],
    # Lesson 489
    [
        ("納采", "のうさい", "betrothal gift (esp. in the Imperial Family)", ["ノウサイ"], []),
        ("釈", "しゃく", "explanation", ["シャク", "セキ"], ["とく", "す.てる", "ゆる.す"]),
        ("解釈", "かいしゃく", "explanation / interpretation", ["カイシャク"], []),
        ("銘", "めい", "inscription / signature (of artisan)", ["メイ"], []),
        ("仰せ", "おおせ", "command / instruction / what one says (honorific)", [], ["おおせ"]),
    ],
    # Lesson 490
    [
        ("銘柄", "めいがら", "brand / make / description (stock)", ["メイガラ"], []),
        ("鋳る", "いる", "to cast / mint / coin", ["チュウ", "イ"], ["い.る"]),
        ("錦", "にしき", "brocade / fine dress / honors", ["キン"], ["にしき"]),
        ("錬", "れん", "tempering / refine / drill / train / polish", ["レン"], ["ね.る"]),
        ("露天風呂", "ろてんぶろ", "open-air bath / outdoor hot spring", ["ロテンブロ"], []),
    ],
    # Lesson 491
    [
        ("精錬", "せいれん", "refining / smelting", ["セイレン"], []),
        ("鎮", "ちん", "tranquilize / ancient peace-preservation centers", ["チン"], ["しず.める", "しず.まる"]),
        ("鎮圧", "ちんあつ", "suppression / subjugation", ["チンアツ"], []),
        ("閲", "えつ", "review / inspection / revision", ["エツ"], ["けみ.する"]),
        ("全裸", "ぜんら", "stark naked / completely nude", ["ゼンラ"], []),
    ],
    # Lesson 492
    [
        ("閲", "えつ", "review / inspection / revision", ["エツ"], ["けみ.する"]),
        ("検閲", "けんえつ", "censorship", ["ケンエツ"], []),
        ("闘", "とう", "fight / war", ["トウ"], ["たたか.う"]),
        ("戦闘", "せんとう", "battle / fight / combat", ["セントウ"], []),
        ("賜物", "たまもの", "gift / boon / result / fruit", [], ["たまもの"]),
    ],
    # Lesson 493
    [
        ("附", "ふ", "affixed / attach / refer to / append", ["フ"], ["つ.ける", "つ.く"]),
        ("陣", "じん", "camp / battle array / ranks / position", ["ジン"], []),
        ("陪", "ばい", "obeisance / follow / accompany / attend on", ["バイ"], []),
        ("陪審", "ばいしん", "jury", ["バイシン"], []),
        ("寄附", "きふ", "contribution / donation", ["キフ"], []),
    ],
    # Lesson 494
    [
        ("隆", "りゅう", "hump / high / noble / prosperity", ["リュウ"], []),
        ("隆盛", "りゅうせい", "prosperity / flourishing / thriving", ["リュウセイ"], []),
        ("隷", "れい", "slave / servant / prisoner / criminal / follower", ["レイ"], ["したが.う", "しもべ"]),
        ("奴隷", "どれい", "slave / servant", ["ドレイ"], []),
        ("漂流", "ひょうりゅう", "drifting / drift / being adrift", ["ヒョウリュウ"], []),
    ],
    # Lesson 495
    [
        ("雌", "めす", "female (animal, plant)", ["シ"], ["め-", "めす", "めん"]),
        ("需", "じゅ", "demand / request / need", ["ジュ"], []),
        ("需要", "じゅよう", "demand / request", ["ジュヨウ"], []),
        ("霜", "しも", "frost", ["ソウ"], ["しも"]),
        ("要塞", "ようさい", "fortress / stronghold / citadel", ["ヨウサイ"], []),
    ],
    # Lesson 496
    [
        ("韻", "いん", "rhyme / elegance / tone", ["イン"], []),
        ("須", "す", "ought / by all means / necessarily", ["ス", "シュ"], ["すべから.く", "もち.いる"]),
        ("必須", "ひっす", "indispensable / essential / required", ["ヒッス"], []),
        ("頒", "はん", "partition / distribute / disseminate / share", ["ハン"], ["わか.つ"]),
        ("宮城", "みやぎ", "Miyagi Prefecture", [], ["みやぎ"]),
    ],
    # Lesson 497
    [
        ("頒布", "はんぷ", "distribution / circulation", ["ハンプ"], []),
        ("餓", "が", "starve / hungry / thirst", ["ガ"], ["う.える"]),
        ("飢餓", "きが", "starvation / famine", ["キガ"], []),
        ("駒", "こま", "piece (in shogi, chess, etc.) / colt / horse / frame", ["ク"], ["こま"]),
        ("川柳", "せんりゅう", "senryu (comic haiku)", ["センリュウ"], []),
    ],
    # Lesson 498
    [
        ("騎", "き", "equestrian / riding on horses / counter for equestrians", ["キ"], []),
        ("騎士", "きし", "knight / horseman", ["キシ"], []),
        ("騰", "とう", "leaping up / jumping up / rising / advancing / going", ["トウ"], ["あが.る", "のぼ.る"]),
        ("高騰", "こうとう", "sudden price jump / steep rise", ["コウトウ"], []),
        ("沸騰", "ふっとう", "boiling / seething", ["フットウ"], []),
    ],
    # Lesson 499
    [
        ("髄", "ずい", "marrow / pith / essence", ["ズイ"], []),
        ("骨髄", "こつずい", "bone marrow / true spirit", ["コツズイ"], []),
        ("鯨", "くじら", "whale", ["ゲイ"], ["くじら"]),
        ("鶏", "にわとり", "chicken", ["ケイ"], ["にわとり", "とり"]),
        ("鶏肉", "とりにく", "chicken meat", ["ケイニク"], ["とりにく"]),
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
    if not os.path.exists(PART3_JSON_PATH):
        raise FileNotFoundError(f"Run 'python generate_n1_part3.py' first to create {PART3_JSON_PATH}.")

    with open(PART3_JSON_PATH, "r", encoding="utf-8") as f:
        lessons = json.load(f)

    item_counter = sum(len(l["items"]) for l in lessons) + 1

    for l_idx, chunk in enumerate(N1_PART4_DATA):
        lesson_num = 377 + l_idx
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

    with open(PART4_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(lessons, f, ensure_ascii=False)

    print(f"Part 4 complete! Saved Lessons 1-499 ({item_counter - 1} items) to {PART4_JSON_PATH}.")


if __name__ == "__main__":
    main()