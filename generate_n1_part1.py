import os
import json
import xml.etree.ElementTree as ET

KANJIVG_DIR = "kanjivg-data"
PART1_JSON_PATH = "n1_part1.json"

N1_PART1_DATA = [
    # Lesson 1[cite: 28]
    [
        ("視", "し", "look at / inspect / regard as", ["シ"], ["み.る"]),
        ("無視", "むし", "disregarding / ignoring", ["ムシ"], []),
        ("独り", "ひとり", "alone / by oneself", ["ドク"], ["ひと.り"]),
        ("独身", "どくしん", "single / unmarried", ["ドクシン"], []),
        ("仕舞う", "しまう", "to put away / finish / close", [], ["しま.う"]),
    ],
    # Lesson 2[cite: 28]
    [
        ("士", "し", "gentleman / samurai / scholar", ["シ"], []),
        ("消防士", "しょうぼうし", "firefighter", ["ショウボウシ"], []),
        ("富士山", "ふじさん", "Mount Fuji", ["フジサン"], []),
        ("結ぶ", "むすぶ", "to tie / bind / link", ["ケツ"], ["むす.ぶ", "ゆ.う"]),
        ("然し", "しかし", "however / but", ["ゼン", "ネン"], ["しか.し"]),
    ],
    # Lesson 3[cite: 28]
    [
        ("結果", "けっか", "result / consequence / outcome", ["ケッカ"], []),
        ("結局", "けっきょく", "after all / eventually", ["ケッキョク"], []),
        ("結婚", "けっこん", "marriage", ["ケッコン"], []),
        ("結論", "けつろん", "conclusion", ["ケツロン"], []),
        ("事業", "じぎょう", "enterprise / business / project", ["ジギョウ"], []),
    ],
    # Lesson 4[cite: 28]
    [
        ("結構", "けっこう", "splendid / nice / quite / enough", ["ケッコウ"], []),
        ("恋愛結婚", "れんあいけっこん", "love marriage", ["レンアイケッコン"], []),
        ("氏", "し", "family name / Mr. / clan", ["シ"], ["うじ"]),
        ("彼氏", "かれし", "boyfriend", [], ["かれし"]),
        ("直ぐ", "すぐ", "immediately / at once / soon", ["チョク", "ジキ"], ["す.ぐ"]),
    ],
    # Lesson 5[cite: 28]
    [
        ("氏名", "しめい", "full name / identity", ["シメイ"], []),
        ("弓", "ゆみ", "bow (and arrow)", ["キュウ"], ["ゆみ"]),
        ("乙", "おつ", "second / latter / strange / quaint", ["オツ"], []),
        ("第", "だい", "ordinal prefix / number", ["ダイ"], []),
        ("共", "とも", "together / both / alike", ["キョウ"], ["とも"]),
    ],
    # Lesson 6[cite: 28]
    [
        ("次第に", "しだいに", "gradually / by degrees", ["シダイ"], []),
        ("第一印象", "だいいちいんしょう", "first impression", ["ダイイチインショウ"], []),
        ("保つ", "たもつ", "to keep / preserve / maintain", ["ホ"], ["たも.つ"]),
        ("保険", "ほけん", "insurance / guarantee", ["ホケン"], []),
        ("返る", "かえる", "to return / come back / turn over", ["ヘン"], ["かえ.る"]),
    ],
    # Lesson 7[cite: 28]
    [
        ("保存", "ほぞん", "preservation / conservation / storage", ["ホゾン"], []),
        ("保育士", "ほいくし", "childcare worker / nursery teacher", ["ホイクシ"], []),
        ("生命保険", "せいめいほけん", "life insurance", ["セイメイホケン"], []),
        ("羊", "ひつじ", "sheep", ["ヨウ"], ["ひつじ"]),
        ("詰まり", "つまり", "in short / in other words / after all", ["キツ"], ["つま.り"]),
    ],
    # Lesson 8[cite: 28]
    [
        ("義", "ぎ", "righteousness / justice / morality", ["ギ"], []),
        ("講義", "こうぎ", "lecture", ["コウギ"], []),
        ("吉", "きち", "good luck / joy / auspicious", ["キチ", "キツ"], ["よし"]),
        ("丼", "どんぶり", "bowl / rice bowl dish", ["トン", "タン"], ["どんぶり"]),
        ("若し", "もし", "if / in case / supposing", ["ジャク"], ["も.し"]),
    ],
    # Lesson 9[cite: 28]
    [
        ("天井", "てんじょう", "ceiling", ["テンジョウ"], []),
        ("汁", "しる", "soup / juice / broth", ["ジュウ"], ["しる"]),
        ("張る", "はる", "to stick / stretch / spread", ["チョウ"], ["は.る"]),
        ("出張", "しゅっちょう", "business trip / official tour", ["シュッチョウ"], []),
        ("かも知れない", "かもしれない", "may / might / perhaps", [], ["し.れない"]),
    ],
    # Lesson 10[cite: 28]
    [
        ("松", "まつ", "pine tree", ["ショウ"], ["まつ"]),
        ("応ずる", "おうずる", "to respond / comply with / accept", ["オウ"], ["おう.ずる"]),
        ("応じる", "おうじる", "to respond / answer / meet", ["オウ"], ["おう.じる"]),
        ("一応", "いちおう", "more or less / tentatively / for now", ["イチオウ"], []),
        ("開発", "かいはつ", "development / exploitation", ["カイハツ"], []),
    ],
    # Lesson 11[cite: 28]
    [
        ("応募", "おうぼ", "application / subscription / entry", ["オウボ"], []),
        ("態", "たい", "attitude / condition / appearance", ["タイ"], ["わざ.と"]),
        ("状態", "じょうたい", "state / condition / situation", ["ジョウタイ"], []),
        ("態度", "たいど", "attitude / manner / demeanor", ["タイド"], []),
        ("規定", "きてい", "regulation / provisions / rules", ["キテイ"], []),
    ],
    # Lesson 12[cite: 28]
    [
        ("心理状態", "しんりじょうたい", "mental state / state of mind", ["シンリジョウタイ"], []),
        ("経済状態", "けいざいじょうたい", "economic condition / financial state", ["ケイザイジョウタイ"], []),
        ("姿", "すがた", "figure / form / shape / appearance", ["シ"], ["すがた"]),
        ("お宮", "おみや", "Shinto shrine", ["キュウ", "グウ"], ["みや"]),
        ("図る", "はかる", "to plan / attempt / devise", ["ト", "ズ"], ["はか.る"]),
    ],
    # Lesson 13[cite: 28]
    [
        ("宮殿", "きゅうでん", "palace", ["キュウデン"], []),
        ("離す", "はなす", "to separate / part / divide", ["リ"], ["はな.す"]),
        ("離れる", "はなれる", "to be separated / leave / move away", ["リ"], ["はな.れる"]),
        ("離婚", "りこん", "divorce", ["リコン"], []),
        ("易い", "やすい", "easy / simple / ready to", ["イ", "エキ"], ["やさ.しい", "やす.い"]),
    ],
    # Lesson 14[cite: 29]
    [
        ("分離", "ぶんり", "separation / detachment / segregation", ["ブンリ"], []),
        ("基", "もと", "basis / foundation / origin", ["キ"], ["もと", "もとい"]),
        ("基", "き", "radical / group / base", ["キ"], ["もと"]),
        ("基づく", "もとづく", "to be grounded on / be based on", ["キ"], ["もと.づく"]),
        ("長", "ちょう", "chief / head / leader / merit", ["チョウ"], ["なが.い"]),
    ],
    # Lesson 15[cite: 29]
    [
        ("基準", "きじゅん", "standard / basis / criterion / norm", ["キジュン"], []),
        ("基金", "ききん", "fund / foundation", ["キキン"], []),
        ("基地", "きち", "base (military, etc.)", ["キチ"], []),
        ("基本", "きほん", "basics / fundamentals / basis", ["キホン"], []),
        ("設定", "せってい", "establishment / creation / setting", ["セッテイ"], []),
    ],
    # Lesson 16[cite: 29]
    [
        ("隊", "たい", "party / company / squad / corps", ["タイ"], []),
        ("兵隊", "へいたい", "soldier / sailor", ["ヘイタイ"], []),
        ("軍隊", "ぐんたい", "armed forces / military / troops", ["グンタイ"], []),
        ("素", "す", "element / principle / unadorned / raw", ["ソ", "ス"], ["もと"]),
        ("正に", "まさに", "exactly / surely / certainly", ["セイ", "ショウ"], ["まさ.に"]),
    ],
    # Lesson 17[cite: 29]
    [
        ("素直", "すなお", "obedient / meek / docile / honest", ["スナオ"], []),
        ("素早い", "すばやい", "fast / quick / nimble / agile", [], ["すばや.い"]),
        ("素晴らしい", "すばらしい", "wonderful / splendid / magnificent", [], ["すば.らしい"]),
        ("価", "あたい", "price / cost / value / worth", ["カ"], ["あたい"]),
        ("価値", "かち", "value / worth / merit", ["カチ"], []),
    ],
    # Lesson 18[cite: 29]
    [
        ("物価", "ぶっか", "prices of commodities / cost of living", ["ブッカ"], []),
        ("又", "また", "again / and / also / moreover", ["ユウ"], ["また"]),
        ("又は", "または", "or / otherwise", ["ユウ"], ["また.は"]),
        ("撃つ", "うつ", "to shoot / fire / attack / defeat", ["ゲキ"], ["う.つ"]),
        ("極めて", "きわめて", "exceedingly / extremely / remarkably", ["キョク"], ["きわ.めて"]),
    ],
    # Lesson 19[cite: 29]
    [
        ("振り", "ふり", "swing / shake / pretense / appearance", ["シン"], ["ふ.り"]),
        ("振る", "ふる", "to wave / shake / swing / reject", ["シン"], ["ふ.る"]),
        ("振り向く", "ふりむく", "to turn one's face / look back", [], ["ふりむ.く"]),
        ("証", "あかし", "proof / evidence / testimony", ["ショウ"], ["あかし"]),
        ("改革", "かいかく", "reform / reorganization / innovation", ["カイカク"], []),
    ],
    # Lesson 20[cite: 29]
    [
        ("保証", "ほしょう", "guarantee / security / assurance", ["ホショウ"], []),
        ("証明", "しょうめい", "proof / verification / certification", ["ショウメイ"], []),
        ("保証書", "ほしょうしょ", "written guarantee / warranty", ["ホショウショ"], []),
        ("保険証", "ほけんしょう", "health insurance card", ["ホケンショウ"], []),
        ("戦", "いくさ", "war / battle / campaign", ["セン"], ["いくさ", "たたか.う"]),
    ],
    # Lesson 21[cite: 29]
    [
        ("証明書", "しょうめいしょ", "certificate / credentials", ["ショウメイショ"], []),
        ("暗証番号", "あんしょうばんごう", "PIN / personal identification number", ["アンショウバンゴウ"], []),
        ("派", "は", "clique / faction / school / party", ["ハ"], []),
        ("派手", "はで", "showy / loud / flashy / gaudy", ["ハデ"], []),
        ("捕らえる", "とらえる", "to catch / capture / seize / arrest", ["ホ"], ["とら.える"]),
    ],
    # Lesson 22[cite: 29]
    [
        ("立派", "りっぱ", "splendid / fine / handsome / respectable", ["リッパ"], []),
        ("僕", "ぼく", "I / me (male)", ["ボク"], ["しもべ"]),
        ("紀", "き", "chronicle / account / era / period", ["キ"], []),
        ("世紀", "せいき", "century / era", ["セイキ"], []),
        ("難い", "かたい", "difficult / hard (to do)", ["ナン"], ["かた.い", "むずか.しい"]),
    ],
    # Lesson 23[cite: 29]
    [
        ("統", "とう", "overall / relationship / ruling", ["トウ"], ["す.べる"]),
        ("大統領", "だいとうりょう", "president (of a nation)", ["ダイトウリョウ"], []),
        ("食器", "しょっき", "tableware / dishes", ["ショッキ"], []),
        ("器", "うつわ", "bowl / vessel / container / ability", ["キ"], ["うつわ"]),
    ],
    # Lesson 24[cite: 29]
    [
        ("器用", "きよう", "skillful / adroit / dexterous / handy", ["キヨウ"], []),
        ("不器用", "ぶきよう", "clumsy / awkward / unskillful", ["ブキヨウ"], []),
        ("異なる", "ことなる", "to differ / vary / disagree", ["イ"], ["こと.なる"]),
        ("異常", "いじょう", "strangeness / abnormality / disorder", ["イジョウ"], []),
        ("器", "き", "utensil / instrument / organ", ["キ"], ["うつわ"]),
    ],
    # Lesson 25[cite: 29]
    [
        ("介護士", "かいごし", "care worker / caregiver", ["カイゴシ"], []),
        ("条", "じょう", "article / clause / item / stripe", ["ジョウ"], ["すじ"]),
        ("条件", "じょうけん", "condition / term / requirement", ["ジョウケン"], []),
        ("護", "ご", "safeguard / protect", ["ゴ"], ["まも.る"]),
    ],
    # Lesson 26[cite: 30]
    [
        ("独立", "どくりつ", "independence / self-reliance", ["ドクリツ"], []),
        ("独特", "どくとく", "peculiarity / uniqueness / characteristic", ["ドクトク"], []),
        ("独占", "どくせん", "monopoly / exclusivity", ["ドクセン"], []),
        ("独自", "どくじ", "original / unique / distinctive", ["ドクジ"], []),
        ("反応", "はんのう", "reaction / response", ["ハンノウ"], []),
    ],
    # Lesson 27[cite: 30]
    [
        ("単独", "たんどく", "sole / single / solo / independent", ["タンドク"], []),
        ("独り言", "ひとりごと", "soliloquy / monologue / talking to oneself", [], ["ひとりごと"]),
        ("源", "みなもと", "source / origin", ["ゲン"], ["みなもと"]),
        ("電源", "でんげん", "source of electricity / power supply", ["デンゲン"], []),
        ("果たす", "はたす", "to accomplish / achieve / carry out", ["カ"], ["は.たす"]),
    ],
    # Lesson 28[cite: 30]
    [
        ("資源", "しげん", "resources", ["シゲン"], []),
        ("影", "かげ", "shadow / silhouette / reflection", ["エイ"], ["かげ"]),
        ("眼", "め", "eye / eyeball", ["ガン", "ゲン"], ["まなこ", "め"]),
        ("眼科", "がんか", "ophthalmology", ["ガンカ"], []),
        ("上昇", "じょうしょう", "rising / ascending / climbing", ["ジョウショウ"], []),
    ],
    # Lesson 29[cite: 30]
    [
        ("眼球", "がんきゅう", "eyeball", ["ガンキュウ"], []),
        ("近眼", "きんがん", "nearsightedness / myopia", ["キンガン"], []),
        ("企て", "くわだて", "plan / plot / scheme / attempt", ["キ"], ["くわだ.て"]),
        ("企業", "きぎょう", "enterprise / business / corporation", ["キギョウ"], []),
        ("雇用", "こよう", "employment / hire", ["コヨウ"], []),
    ],
    # Lesson 30[cite: 30]
    [
        ("津", "つ", "haven / port / harbor / ferry", ["シン"], ["つ"]),
        ("津波", "つなみ", "tsunami / tidal wave", [], ["つなみ"]),
        ("案", "あん", "idea / plan / proposal / draft", ["アン"], []),
        ("案じる", "あんじる", "to be anxious / worry about / ponder", ["アン"], ["あん.じる"]),
        ("訪れる", "おとずれる", "to visit / call on / arrive", ["ホウ"], ["おとず.れる"]),
    ],
    # Lesson 31[cite: 30]
    [
        ("案外", "あんがい", "unexpectedly / surprisingly", ["アンガイ"], []),
        ("案内", "あんない", "information / guidance / leading", ["アンナイ"], []),
        ("巾", "はば", "towel / hanging scroll / width", ["キン", "フク"], ["はば"]),
        ("雑巾", "ぞうきん", "house-cloth / dust cloth / rag", ["ゾウキン"], []),
        ("利く", "きく", "to be effective / work / function well", ["リ"], ["き.く"]),
    ],
    # Lesson 32[cite: 30]
    [
        ("策", "さく", "scheme / plan / policy / stratagem", ["サク"], []),
        ("政策", "せいさく", "political measures / policy", ["セイサク"], []),
        ("対策", "たいさく", "countermeasure / step / policy", ["タイサク"], []),
        ("方策", "ほうさく", "plan / policy / measure", ["ホウサク"], []),
        ("初", "はつ", "first / new / beginning", ["ショ"], ["はじ.め", "はつ", "うい"]),
    ],
    # Lesson 33[cite: 30]
    [
        ("宗", "しゅう", "religion / sect / denomination", ["シュウ", "ソウ"], ["むね"]),
        ("宗教", "しゅうきょう", "religion / religious faith", ["シュウキョウ"], []),
        ("提", "てい", "propose / take along / carry in hand", ["テイ"], ["さ.げる"]),
        ("提出", "ていしゅつ", "presentation / submission / filing", ["テイシュツ"], []),
        ("提供", "ていきょう", "offer / tender / providing / supplying", ["テイキョウ"], []),
    ],
    # Lesson 34[cite: 30]
    [
        ("刀", "かたな", "sword / saber / knife / katana", ["トウ"], ["かたな"]),
        ("密か", "ひそか", "secret / private / stealthy", ["ミツ"], ["ひそ.か"]),
        ("密度", "みつど", "density", ["ミツド"], []),
        ("密接", "みっせつ", "related / connected / close / intimate", ["ミッセツ"], []),
        ("背景", "はいけい", "background / scenery / backdrop", ["ハイケイ"], []),
    ],
    # Lesson 35[cite: 30]
    [
        ("過密", "かみつ", "overcrowded / congested", ["カミツ"], []),
        ("精密", "せいみつ", "precise / exact / detailed / minute", ["セイミツ"], []),
        ("密集", "みっしゅう", "crowd / close formation / dense", ["ミッシュウ"], []),
        ("司", "つかさ", "director / official / govt office / rule", ["シ"], ["つかさ"]),
        ("姿勢", "しせい", "posture / pose / attitude", ["シセイ"], []),
    ],
    # Lesson 36[cite: 30]
    [
        ("上司", "じょうし", "one's superior / boss", ["ジョウシ"], []),
        ("司会", "しかい", "master of ceremonies / chairperson / host", ["シカイ"], []),
        ("お寿司", "おすし", "sushi", ["スシ"], []),
        ("司会者", "しかいしゃ", "host / master of ceremonies / moderator", ["シカイシャ"], []),
        ("記す", "しるす", "to note / write down / record", ["キ"], ["しる.す"]),
    ],
    # Lesson 37[cite: 30]
    [
        ("ヤメ検", "ヤメけん", "former public prosecutor (now a lawyer)", ["ケン"], []),
        ("検査", "けんさ", "inspection / examination / scan / test", ["ケンサ"], []),
        ("沢", "さわ", "swamp / marsh / mountain stream", ["タク"], ["さわ"]),
        ("金沢", "かなざわ", "Kanazawa", [], ["かなざわ"]),
        ("沢山", "たくさん", "a lot / lots / plenty / many / much", ["タクサン"], []),
    ],
    # Lesson 38[cite: 30]
    [
        ("秀でる", "ひいでる", "to excel / surpass / be prominent", ["シュウ"], ["ひい.でる"]),
        ("優秀", "ゆうしゅう", "superiority / excellence", ["ユウシュウ"], []),
        ("興じる", "きょうじる", "to amuse oneself / make merry", ["キョウ", "コウ"], ["きょう.じる"]),
        ("興味", "きょうみ", "interest (in something) / curiosity", ["キョウミ"], []),
        ("経る", "へる", "to pass / elapse / go through", ["ケイ", "キョウ"], ["へ.る", "た.つ"]),
    ],
    # Lesson 39[cite: 30]
    [
        ("玄関", "げんかん", "entranceway / entry hall / vestibule", ["ゲンカン"], []),
        ("率", "りつ", "rate / ratio / proportion / percentage", ["リツ", "ソツ"], ["ひき.いる"]),
        ("率いる", "ひきいる", "to lead / spearhead / command", ["ソツ", "リツ"], ["ひき.いる"]),
        ("比率", "ひりつ", "ratio / proportion / percentage", ["ヒリツ"], []),
        ("玄", "げん", "mysterious / occultness / black / deep", ["ゲン"], []),
    ],
    # Lesson 40[cite: 31]
    [
        ("効率", "こうりつ", "efficiency", ["コウリツ"], []),
        ("率直", "そっちょく", "frank / candid / straightforward / open", ["ソッチョク"], []),
        ("軽率", "けいそつ", "rash / thoughtless / careless / hasty", ["ケイソツ"], []),
        ("倍率", "ばいりつ", "magnification / leverage / competition ratio", ["バイリツ"], []),
        ("固定", "こてい", "fixing (in place) / fastening / stationary", ["コテイ"], []),
    ],
    # Lesson 41[cite: 31]
    [
        ("確率", "かくりつ", "probability / likelihood / chances", ["カクリツ"], []),
        ("能率", "のうりつ", "efficiency", ["ノウリツ"], []),
        ("統率", "とうそつ", "command / lead / generalship / leadership", ["トウソツ"], []),
        ("評", "ひょう", "criticism / critique / reputation", ["ヒョウ"], []),
        ("重", "じゅう", "heavy / important / layer / fold", ["ジュウ", "チョウ"], ["おも.い", "かさ.ねる"]),
    ],
    # Lesson 42[cite: 31]
    [
        ("評判", "ひょうばん", "fame / reputation / popularity", ["ヒョウバン"], []),
        ("監", "かん", "oversee / official / govt office / rule", ["カン"], []),
        ("長崎", "ながさき", "Nagasaki", [], ["ながさき"]),
        ("鮮やか", "あざやか", "vivid / bright / brilliant / skillful", ["セン"], ["あざ.やか"]),
        ("崎", "さき", "promontory / cape / spit", ["キ"], ["さき"]),
    ],
    # Lesson 43[cite: 31]
    [
        ("新鮮", "しんせん", "fresh", ["シンセン"], []),
        ("激しい", "はげしい", "violent / furious / tempestuous / intense", ["ゲキ"], ["はげ.しい"]),
        ("感激", "かんげき", "deep emotion / impression / inspiration", ["カンゲキ"], []),
        ("徳", "とく", "benevolence / virtue / goodness", ["トク"], []),
        ("群", "ぐん", "flock / group / crowd / herd", ["グン"], ["む.れる", "むれ"]),
    ],
    # Lesson 44[cite: 31]
    [
        ("道徳", "どうとく", "morals / morality", ["ドウトク"], []),
        ("尚更", "なおさら", "all the more / still less", ["ショウ"], ["なおさら"]),
        ("高尚", "こうしょう", "high / noble / refined / advanced", ["コウショウ"], []),
        ("尚", "なお", "furthermore / still / yet / more", ["ショウ"], ["なお"]),
    ],
    # Lesson 45[cite: 31]
    [
        ("挙げる", "あげる", "to raise / fly / give (an example)", ["キョ"], ["あ.げる", "あ.がる"]),
        ("選挙", "せんきょ", "election", ["センキョ"], []),
        ("一挙に", "いっきょに", "at a stroke / with a single effort / all at once", ["イッキョ"], []),
        ("志", "こころざし", "will / resolution / intention / ambition", ["シ"], ["こころざ.す", "こころざし"]),
        ("未", "み", "un- / not yet / hitherto / still", ["ミ", "ビ"], ["いま.だ", "ま.だ"]),
    ],
    # Lesson 46[cite: 31]
    [
        ("志す", "こころざす", "to plan / intend / aspire to / set aims", ["シ"], ["こころざ.す"]),
        ("志望", "しぼう", "wish / desire / ambition", ["シボウ"], []),
        ("意志", "いし", "will / volition / intention / mind", ["イシ"], []),
        ("同志", "どうし", "same mind / comrade / kindred soul", ["ドウシ"], []),
        ("振興", "しんこう", "promotion / encouragement / development", ["シンコウ"], []),
    ],
    # Lesson 47[cite: 31]
    [
        ("志向", "しこう", "intention / aim / preference / orientation", ["シコウ"], []),
        ("敷く", "しく", "to spread out / lay out", ["フ"], ["し.く"]),
        ("系", "けい", "lineage / system", ["ケイ"], []),
        ("文系", "ぶんけい", "humanities / social sciences / liberal arts", ["ブンケイ"], []),
        ("歩", "ぶ", "rate / percentage / step / pawn (shogi)", ["ホ", "ブ", "フ"], ["ある.く", "あゆ.む"]),
    ],
    # Lesson 48[cite: 31]
    [
        ("理系", "りけい", "science (as a field of study)", ["リケイ"], []),
        ("織", "おり", "weave / weaving / woven item", ["ショク", "シキ"], ["お.る"]),
        ("織る", "おる", "to weave", ["ショク", "シキ"], ["お.る"]),
        ("組織", "そしき", "organization / structure / tissue", ["ソシキ"], []),
    ],
    # Lesson 49[cite: 31]
    [
        ("織物", "おりもの", "textile / fabric", [], ["おりもの"]),
        ("刈る", "かる", "to cut (hair) / mow (grass) / harvest", ["ガイ", "カイ"], ["か.る"]),
        ("製品", "せいひん", "manufactured goods / finished goods / product", ["セイヒン"], []),
        ("日本製", "にほんせい", "made in Japan", ["ニホンセイ"], []),
        ("製", "せい", "-made / make", ["セイ"], []),
    ],
    # Lesson 50[cite: 31]
    [
        ("端", "はし", "end (e.g. of street) / tip / edge / margin", ["タン"], ["はし", "は", "はた"]),
        ("途端", "とたん", "just (now, at the moment, etc.)", ["トタン"], []),
        ("世界遺産", "せかいいさん", "World Heritage (cultural, natural, etc.)", ["セカイイサン"], []),
        ("房", "ふさ", "tuft / tassel / fringe / cluster / segment", ["ボウ"], ["ふさ"]),
        ("遺", "い", "bequeath / leave behind / reserve", ["イ", "ユイ"], ["のこ.す"]),
    ],
    # Lesson 51[cite: 32]
    [
        ("冷房", "れいぼう", "air conditioning / air cooling", ["レイボウ"], []),
        ("街", "まち", "town / block / neighborhood / street", ["ガイ", "カイ"], ["まち"]),
        ("商店街", "しょうてんがい", "shopping district / shopping street", ["ショウテンガイ"], []),
        ("尾", "お", "tail / ridge / tail end", ["ビ"], ["お"]),
        ("著しい", "いちじるしい", "conspicuous / remarkable / striking", ["チョ"], ["いちじる.しい"]),
    ],
    # Lesson 52[cite: 32]
    [
        ("株", "かぶ", "share / stock / stump (of tree)", ["シュ"], ["かぶ"]),
        ("株式", "かぶしき", "stock (company)", ["カブシキ"], []),
        ("従う", "したがう", "to obey / follow / accompany / comply", ["ジュウ", "ショウ"], ["したが.う"]),
        ("従って", "したがって", "therefore / consequently / accordingly", ["ジュウ"], ["したが.って"]),
        ("一切", "いっさい", "all / everything / without exception", ["イッサイ"], []),
    ],
    # Lesson 53[cite: 32]
    [
        ("従事", "じゅうじ", "engaging in / pursuing / following", ["ジュウジ"], []),
        ("従来", "じゅうらい", "up to now / so far / traditional", ["ジュウライ"], []),
        ("従兄弟", "いとこ", "cousin (male)", ["ジュウケイ"], ["いとこ"]),
        ("従業員", "じゅうぎょういん", "employee / worker", ["ジュウギョウイン"], []),
        ("巻", "かん", "scroll / volume / book / reel", ["カン", "ケン"], ["ま.く", "まき"]),
    ],
    # Lesson 54[cite: 32]
    [
        ("従姉妹", "いとこ", "cousin (female)", ["ジュウシマイ"], ["いとこ"]),
        ("敵", "てき", "opponent / rival / adversary / enemy", ["テキ"], ["かたき", "あだ"]),
        ("素敵", "すてき", "lovely / wonderful / nice / great", ["ステキ"], []),
        ("怒り", "いかり", "anger / rage / fury / wrath", ["ド"], ["いか.り", "おこ.る"]),
        ("負う", "おう", "to bear / carry on one's back / owe", ["フ"], ["お.う"]),
    ],
    # Lesson 55[cite: 32]
    [
        ("展", "てん", "exhibition / display", ["テン"], []),
        ("発展", "はってん", "development / growth / expansion", ["ハッテン"], []),
        ("描く", "えがく", "to draw / paint / sketch / depict", ["ビョウ"], ["えが.く", "か.く"]),
        ("修める", "おさめる", "to study / complete (a course) / master", ["シュウ", "シュ"], ["おさ.める"]),
        ("久し振り", "ひさしぶり", "a long time (since the last time)", [], ["ひさしぶり"]),
    ],
    # Lesson 56[cite: 32]
    [
        ("修理", "しゅうり", "repair / mending / fixing / servicing", ["シュウリ"], []),
        ("研修", "けんしゅう", "training (esp. in-service) / induction", ["ケンシュウ"], []),
        ("我がまま", "わがまま", "selfishness / egoism / wilfulness", [], ["わがまま"]),
        ("自我", "じが", "ego / the self", ["ジガ"], []),
        ("我々", "われわれ", "we", [], ["われわれ"]),
    ],
    # Lesson 57[cite: 32]
    [
        ("載る", "のる", "to appear (in print) / be recorded / be loaded", ["サイ"], ["の.る"]),
        ("載せる", "のせる", "to place on / put on / publish / load", ["サイ"], ["の.せる"]),
        ("記載", "きさい", "mention / entry / recording / listing", ["キサイ"], []),
        ("響く", "ひびく", "to resound / be heard far away / reverberate", ["キョウ"], ["ひび.く"]),
        ("株主", "かぶぬし", "shareholder / stockholder", [], ["かぶぬし"]),
    ],
    # Lesson 58[cite: 32]
    [
        ("響き", "ひびき", "echo / reverberation / sound / ring", ["キョウ"], ["ひび.き"]),
        ("影響", "えいきょう", "influence / effect", ["エイキョウ"], []),
        ("秘める", "ひめる", "to hide / keep to oneself / conceal", ["ヒ"], ["ひ.める"]),
        ("秘密", "ひみつ", "secret / secrecy / confidentiality", ["ヒミツ"], []),
        ("相応しい", "ふさわしい", "appropriate / adequate / suitable", [], ["ふさわ.しい"]),
    ],
    # Lesson 59[cite: 32]
    [
        ("攻め", "せめ", "attack / offense", ["コウ"], ["せ.め"]),
        ("攻める", "せめる", "to attack / assault / assail", ["コウ"], ["せ.める"]),
        ("専攻", "せんこう", "major subject / special study", ["センコウ"], []),
        ("健やか", "すこやか", "vigorous / healthy / sound", ["ケン"], ["すこ.やか"]),
        ("攻撃", "こうげき", "attack / strike / offensive / criticism", ["コウゲキ"], []),
    ],
    # Lesson 60[cite: 32]
    [
        ("健康", "けんこう", "health / sound / wholesome", ["ケンコウ"], []),
        ("健康保険証", "けんこうほけんしょう", "health insurance card", ["ケンコウホケンショウ"], []),
        ("裁く", "さばく", "to judge", ["サイ"], ["さば.く"]),
        ("裁判", "さいばん", "trial / judgment", ["サイバン"], []),
        ("康", "こう", "ease / peace", ["コウ"], []),
    ],
    # Lesson 61[cite: 32]
    [
        ("制裁", "せいさい", "restraints / sanctions / punishment", ["セイサイ"], []),
        ("体裁", "ていさい", "decency / style / form / appearance", ["テイサイ"], []),
        ("独裁", "どくさい", "dictatorship / despotism / autocracy", ["ドクサイ"], []),
        ("隠す", "かくす", "to hide / conceal", ["イン"], ["かく.す", "かく.れる"]),
        ("燃料", "ねんりょう", "fuel", ["ネンリョウ"], []),
    ],
    # Lesson 62[cite: 32]
    [
        ("隠れる", "かくれる", "to hide / be hidden / conceal oneself", ["イン"], ["かく.れる"]),
        ("隠居", "いんきょ", "retirement / retired person", ["インキョ"], []),
        ("環", "かん", "ring / circle / link / wheel", ["カン"], ["わ"]),
        ("環境", "かんきょう", "environment / circumstance", ["カンキョウ"], []),
        ("身近", "みぢか", "near oneself / close to one / familiar", [], ["みぢか"]),
    ],
    # Lesson 63[cite: 32]
    [
        ("爪", "つめ", "nail (finger or toe) / claw / talon", ["ソウ"], ["つめ", "つま"]),
        ("応援", "おうえん", "aid / assistance / help / cheering", ["オウエン"], []),
        ("故", "ゆえ", "reason / cause / circumstances", ["コ"], ["ゆえ"]),
        ("事故", "じこ", "accident / incident / trouble", ["ジコ"], []),
        ("援", "えん", "abet / help / save", ["エン"], []),
    ],
    # Lesson 64[cite: 33]
    [
        ("事故現場", "じこげんば", "scene of an accident", ["ジコゲンバ"], []),
        ("幕", "まく", "curtain / bunting / act (in play)", ["マク", "バク"], []),
        ("督する", "とくする", "to command / supervise / urge", ["トク"], ["とく.する"]),
        ("施す", "ほどこす", "to give (charity) / apply / perform", ["シ", "セ"], ["ほどこ.す"]),
        ("何故", "なぜ", "why / how", [], ["なぜ"]),
    ],
    # Lesson 65[cite: 33]
    [
        ("嫌", "いや", "disagreeable / detestable / unpleasant", ["ケン", "ゲン"], ["きら.う", "いや"]),
        ("嫌い", "きらい", "disliked / hated / disagreeable", ["ケン"], ["きら.い"]),
        ("嫌がる", "いやがる", "to hate / dislike", ["ケン"], ["いや.がる"]),
        ("機嫌", "きげん", "humor / temper / mood / spirits", ["キゲン"], []),
        ("実施", "じっし", "enforcement / implementation / carrying out", ["ジッシ"], []),
    ],
    # Lesson 66[cite: 33]
    [
        ("上機嫌", "じょうきげん", "good humor / good mood", ["ジョウキゲン"], []),
        ("不機嫌", "ふきげん", "pout / displeasure / ill humor / sullenness", ["フキゲン"], []),
        ("継ぐ", "つぐ", "to succeed (a person, to a position) / inherit", ["ケイ"], ["つ.ぐ"]),
        ("障る", "さわる", "to hinder / interfere with / affect / harm", ["ショウ"], ["さわ.る"]),
        ("施設", "しせつ", "institution / establishment / facility", ["シセツ"], []),
    ],
    # Lesson 67[cite: 33]
    [
        ("故障", "こしょう", "breakdown / out of order / failure", ["コショウ"], []),
        ("貴", "き", "precious / value / prize / esteem / honor", ["キ"], ["たっと.い", "とうと.い"]),
        ("貴族", "きぞく", "noble / aristocrat / peer", ["キゾク"], []),
        ("貴重", "きちょう", "precious / valuable", ["キチョウ"], []),
        ("監督", "かんとく", "supervision / control / director / coach", ["カントク"], []),
    ],
    # Lesson 68[cite: 33]
    [
        ("貴女", "あなた", "you (feminine)", ["キジョ"], ["あなた"]),
        ("整う", "ととのう", "to be prepared / be in order / be arranged", ["セイ"], ["ととの.う"]),
        ("整える", "ととのえる", "to put in order / arrange / adjust / prepare", ["セイ"], ["ととの.える"]),
        ("整理", "せいり", "sorting / arrangement / organization / putting in order", ["セイリ"], []),
        ("継続", "けいぞく", "continuation", ["ケイゾク"], []),
    ],
    # Lesson 69[cite: 33]
    [
        ("調整", "ちょうせい", "regulation / adjustment / tuning / coordination", ["チョウセイ"], []),
        ("衆", "しゅう", "masses / multitude / populace", ["シュウ", "シュ"], ["おお.い"]),
        ("衆議院", "しゅうぎいん", "House of Representatives (lower house)", ["シュウギイン"], []),
        ("及ぶ", "およぶ", "to reach / amount to / befall / match", ["キュウ"], ["およ.ぶ", "およ.ぼす"]),
        ("担う", "になう", "to carry on shoulder / bear (burden) / take on", ["タン"], ["にな.う", "かつ.ぐ"]),
    ],
    # Lesson 70[cite: 33]
    [
        ("及び", "および", "and / as well as", ["キュウ"], ["およ.び"]),
        ("及ぼす", "およぼす", "to exert (influence) / exercise / cause", ["キュウ"], ["およ.ぼす"]),
        ("追及", "ついきゅう", "investigation (e.g. into responsibility) / pressing", ["ツイキュウ"], []),
        ("普及", "ふきゅう", "diffusion / spread / popularization", ["フキュウ"], []),
        ("幕府", "ばくふ", "shogunate / bakufu", ["バクフ"], []),
    ],
    # Lesson 71[cite: 33]
    [
        ("盛ん", "さかん", "popular / prosperous / thriving / active", ["セイ", "ジョウ"], ["さか.ん", "も.る"]),
        ("恵み", "めぐみ", "blessing / grace", ["ケイ"], ["めぐ.み"]),
        ("恵む", "めぐむ", "to bless / show mercy to", ["ケイ"], ["めぐ.む"]),
        ("恵まれる", "めぐまれる", "to be blessed with / be rich in", ["ケイ"], ["めぐ.まれる"]),
        ("側面", "そくめん", "side / flank / profile / lateral", ["ソクメン"], []),
    ],
    # Lesson 72[cite: 33]
    [
        ("知恵", "ちえ", "wisdom / wit / sagacity / sense", ["チエ"], []),
        ("授ける", "さずける", "to grant / confer / award / teach", ["ジュ"], ["さず.ける", "さず.かる"]),
        ("授業", "じゅぎょう", "lesson / class work / teaching / instruction", ["ジュギョウ"], []),
        ("教授", "きょうじゅ", "professor / teaching / instruction", ["キョウジュ"], []),
        ("有難い", "ありがたい", "grateful / thankful / welcome / appreciated", [], ["ありがた.い"]),
    ],
    # Lesson 73[cite: 33]
    [
        ("授業料", "じゅぎょうりょう", "tuition fee / school fee", ["ジュギョウリョウ"], []),
        ("弾く", "ひく", "to play (a stringed or keyboard instrument)", ["ダン"], ["ひ.く", "はじ.く"]),
        ("養う", "やしなう", "to support / maintain / provide for / raise", ["ヨウ"], ["やしな.う"]),
        ("栄養", "えいよう", "nutrition / nourishment", ["エイヨウ"], []),
        ("屋敷", "やしき", "residence / estate / grounds / mansion", [], ["やしき"]),
    ],
    # Lesson 74[cite: 33]
    [
        ("驚く", "おどろく", "to be surprised / be astonished", ["キョウ"], ["おどろ.く"]),
        ("奈良", "なら", "Nara", [], ["なら"]),
        ("推す", "おす", "to recommend / endorse / infer / deduce", ["スイ"], ["お.す"]),
        ("推進", "すいしん", "propulsion / drive / promotion", ["スイシン"], []),
        ("奈", "な", "Nara / what?", ["ナ", "ナイ", "ダイ"], ["いかん"]),
    ],
    # Lesson 75[cite: 33]
    [
        ("推理", "すいり", "reasoning / inference / deduction / mystery", ["スイリ"], []),
        ("類推", "るいすい", "analogy", ["ルイスイ"], []),
        ("推定", "すいてい", "presumption / assumption / estimation", ["スイテイ"], []),
        ("推測", "すいそく", "guess / conjecture", ["スイソク"], []),
        ("河川", "かせん", "rivers", ["カセン"], []),
    ],
    # Lesson 76[cite: 33]
    [
        ("寸", "すん", "measurement / tenth of a shaku (~3.03 cm)", ["スン"], []),
        ("豆", "まめ", "beans / peas", ["トウ", "ズ"], ["まめ"]),
        ("為", "ため", "good / advantage / benefit / sake / purpose", ["イ"], ["ため"]),
        ("為す", "なす", "to build up / establish / form / do", ["イ"], ["な.す"]),
        ("一寸", "ちょっと", "a little / a bit / just a minute", ["イッスン"], ["ちょっと"]),
    ],
    # Lesson 77[cite: 34]
    [
        ("為る", "する", "to do / carry out / perform", ["イ"], ["す.る"]),
        ("為る", "なる", "to become / get / grow / turn", ["イ"], ["な.る"]),
        ("為さる", "なさる", "to do (honorific)", ["イ"], ["なさ.る"]),
        ("その為", "そのため", "hence / for that reason", [], ["そのため"]),
        ("僕達", "ぼくたち", "we / us (masculine)", ["ボク"], ["ぼくたち"]),
    ],
    # Lesson 78[cite: 34]
    [
        ("行為", "こうい", "act / deed / conduct", ["コウイ"], []),
        ("所為", "せい", "consequence / outcome / result / blame", ["ショイ"], ["せい"]),
        ("為替", "かわせ", "money order / exchange", [], ["かわせ"]),
        ("為来り", "しきたり", "custom / conventional practice / tradition", [], ["しきたり"]),
        ("若干", "じゃっかん", "some / few / number of", ["ジャッカン"], []),
    ],
    # Lesson 79[cite: 34]
    [
        ("雄", "おす", "male (animal, plant) / hero / leader", ["ユウ"], ["お-", "おす", "おん"]),
        ("弁", "べん", "speech / dialect / valve / petal / bento", ["ベン", "ヘン"], ["わきま.える"]),
        ("お弁当", "おべんとう", "bento / Japanese box lunch", ["ベントウ"], []),
        ("弁護士", "べんごし", "lawyer / attorney", ["ベンゴシ"], []),
        ("説く", "とく", "to explain / advocate / preach / persuade", ["セツ", "ゼイ"], ["と.く"]),
    ],
    # Lesson 80[cite: 34]
    [
        ("妙", "みょう", "strange / unusual / clever / miraculous", ["ミョウ", "ビョウ"], ["たえ"]),
        ("模す", "もす", "to imitate / copy / mock", ["モ", "ボ"], ["も.する"]),
        ("模様", "もよう", "pattern / figure / design / look / state", ["モヨウ"], []),
        ("模様替え", "もようがえ", "redecoration / rearranging furniture", [], ["もようがえ"]),
        ("規模", "きぼ", "scale / scope / plan / structure", ["キボ"], []),
    ],
    # Lesson 81[cite: 34]
    [
        ("抗", "こう", "confront / resist / defy / oppose", ["コウ"], ["あらが.う"]),
        ("反抗", "はんこう", "opposition / resistance / insubordination / rebellion", ["ハンコウ"], []),
        ("抗争", "こうそう", "dispute / resistance / rivalry / feud", ["コウソウ"], []),
        ("対抗", "たいこう", "opposition / antagonism / rivalry", ["タイコウ"], []),
        ("復活", "ふっかつ", "revival / resurrection / restoration", ["フッカツ"], []),
    ],
    # Lesson 82[cite: 34]
    [
        ("抗議", "こうぎ", "protest / objection", ["コウギ"], []),
        ("級", "きゅう", "class / grade / rank", ["キュウ"], []),
        ("高級", "こうきゅう", "high-class / high-grade / luxury", ["コウキュウ"], []),
        ("瞬き", "まばたき", "wink / twinkling (of stars) / flicker", ["シュン"], ["まばた.き"]),
        ("瞬間", "しゅんかん", "moment / second / instant", ["シュンカン"], []),
    ],
    # Lesson 83[cite: 34]
    [
        ("称する", "しょうする", "to take the name of / call oneself / claim", ["ショウ"], ["しょう.する", "たた.える"]),
        ("名称", "めいしょう", "name / title", ["メイショウ"], []),
        ("華やか", "はなやか", "showy / brilliant / gorgeous / splendid", ["カ", "ケ"], ["はな.やか"]),
        ("華美", "かび", "pomp / splendor / gaudiness", ["カビ"], []),
        ("交わす", "かわす", "to exchange (messages, greetings, glances)", ["コウ"], ["か.わす"]),
    ],
    # Lesson 84[cite: 34]
    [
        ("傷", "きず", "wound / injury / cut / scratch / bruise", ["ショウ"], ["きず", "いた.む"]),
        ("筋", "すじ", "muscle / tendon / sinew / line / plot", ["キン"], ["すじ"]),
        ("筋肉", "きんにく", "muscle", ["キンニク"], []),
        ("大筋", "おおすじ", "outline / summary / main points", [], ["おおすじ"]),
        ("試みる", "こころみる", "to try / test / attempt", ["シ"], ["こころ.みる"]),
    ],
    # Lesson 85[cite: 34]
    [
        ("訳", "わけ", "conclusion from reasoning / reason / meaning", ["ヤク"], ["わけ"]),
        ("訳", "やく", "translation / version", ["ヤク"], ["わけ"]),
        ("訳す", "やくす", "to translate / interpret", ["ヤク"], ["やく.す"]),
        ("通訳", "つうやく", "interpretation (oral translation)", ["ツウヤク"], []),
        ("不可欠", "ふかけつ", "indispensable / essential", ["フカケツ"], []),
    ],
    # Lesson 86[cite: 34]
    [
        ("射す", "さす", "to shine / strike (light)", ["シャ"], ["さ.す", "い.る"]),
        ("注射", "ちゅうしゃ", "injection / shot", ["チュウシャ"], []),
        ("善", "ぜん", "virtuous / good / goodness", ["ゼン"], ["よ.い", "い.い"]),
        ("最善", "さいぜん", "the very best", ["サイゼン"], []),
        ("接触", "せっしょく", "touch / contact", ["セッショク"], []),
    ],
    # Lesson 87[cite: 34]
    [
        ("黙る", "だまる", "to be silent", ["モク", "ボク"], ["だま.る"]),
        ("沈黙", "ちんもく", "silence / reticence", ["チンモク"], []),
        ("柄", "がら", "pattern / design / build / character", ["ヘイ"], ["がら", "え"]),
        ("刑", "けい", "punish / penalty / sentence / punishment", ["ケイ"], []),
        ("血管", "けっかん", "blood vessel / vein", ["ケッカン"], []),
    ],
    # Lesson 88[cite: 34]
    [
        ("死刑", "しけい", "death penalty / capital punishment", ["シケイ"], []),
        ("刑事", "けいじ", "police detective / criminal matter", ["ケイジ"], []),
        ("節", "ふし", "joint / knuckle / tune / melody / point", ["セツ", "セチ"], ["ふし"]),
        ("節", "せつ", "occasion / time / season / section", ["セツ"], ["ふし"]),
        ("担保", "たんぽ", "security / guarantee / collateral", ["タンポ"], []),
    ],
    # Lesson 89[cite: 35]
    [
        ("季節", "きせつ", "season / time of year", ["キセツ"], []),
        ("節約", "せつやく", "economising / saving", ["セツヤク"], []),
        ("脱ぐ", "ぬぐ", "to take off (clothes, shoes, etc.)", ["ダツ"], ["ぬ.ぐ", "ぬ.げる"]),
        ("厳しい", "きびしい", "severe / strict / rigid / intense", ["ゲン", "ゴン"], ["きび.しい", "おごそ.か"]),
        ("客観", "きゃっかん", "objectivity / objective", ["キャッカン"], []),
    ],
    # Lesson 90[cite: 35]
    [
        ("博", "はく", "Dr. / command / esteem / win / Ph.D.", ["ハク", "バク"], []),
        ("博物館", "はくぶつかん", "museum", ["ハクブツカン"], []),
        ("奇", "き", "strange / strangeness / curiosity", ["キ"], ["く.しき", "めずら.しい"]),
        ("好奇心", "こうきしん", "curiosity / inquisitiveness", ["コウキシン"], []),
        ("博士", "はかせ", "doctorate / PhD / Dr. / expert", ["ハカセ", "ハクシ"], []),
    ],
    # Lesson 91[cite: 35]
    [
        ("忠", "ちゅう", "loyalty / devotion / fidelity / faithfulness", ["チュウ"], []),
        ("忠実", "ちゅうじつ", "faithful / devoted / loyal / honest / true", ["チュウジツ"], []),
        ("忠告", "ちゅうこく", "advice / warning", ["チュウコク"], []),
        ("染める", "そめる", "to dye / color", ["セン"], ["そ.める", "そ.まる"]),
        ("感染", "かんせん", "infection / contagion", ["カンセン"], []),
    ],
    # Lesson 92[cite: 35]
    [
        ("微か", "かすか", "faint / dim / weak / slight / vague", ["ビ"], ["かす.か"]),
        ("微妙", "びみょう", "subtle / delicate / fine / tricky", ["ビミョウ"], []),
        ("微笑み", "ほほえみ", "smile", ["ビ"], ["ほほえ.み"]),
        ("微笑む", "ほほえむ", "to smile", ["ビ"], ["ほほえ.む"]),
        ("汚染", "おせん", "pollution / contamination", ["オセン"], []),
    ],
    # Lesson 93[cite: 35]
    [
        ("プリムソル標", "プリムソルひょう", "Plimsoll mark / Plimsoll line", ["ヒョウ"], []),
        ("標準", "ひょうじゅん", "standard / level / norm", ["ヒョウジュン"], []),
        ("目標", "もくひょう", "mark / objective / target / goal", ["モクヒョウ"], []),
        ("標語", "ひょうご", "motto / slogan / catchword", ["ヒョウゴ"], []),
        ("説得", "せっとく", "persuasion", ["セットク"], []),
    ],
    # Lesson 94[cite: 35]
    [
        ("標本", "ひょうほん", "example / specimen / sample", ["ヒョウホン"], []),
        ("座標", "ざひょう", "coordinate / coordinates", ["ザヒョウ"], []),
        ("標識", "ひょうしき", "sign / mark / beacon / landmark", ["ヒョウシキ"], []),
        ("縁", "えん", "affinity / relation / connection / edge / fate", ["エン"], ["ふち"]),
        ("心掛ける", "こころがける", "to bear in mind / aim to do / keep in mind", [], ["こころが.ける"]),
    ],
    # Lesson 95[cite: 35]
    [
        ("縁談", "えんだん", "marriage proposal / marriage talk", ["エンダン"], []),
        ("縁側", "えんがわ", "veranda / porch / balcony", [], ["えんがわ"]),
        ("壁", "かべ", "wall / partition / barrier", ["ヘキ"], ["かべ"]),
        ("駆ける", "かける", "to run (race, esp. horse) / gallop / canter", ["ク"], ["か.ける", "か.る"]),
        ("逃れる", "のがれる", "to escape", ["トウ"], ["のが.れる", "に.げる"]),
    ],
    # Lesson 96[cite: 35]
    [
        ("駆けっこ", "かけっこ", "(foot) race", [], ["かけっこ"]),
        ("麻", "あさ", "hemp / flax / linen", ["マ"], ["あさ"]),
        ("甲", "こう", "armor / high (voice) / A (grade) / instep", ["コウ", "カン"], ["きのえ"]),
        ("迫る", "せまる", "to approach / draw near / press / urge", ["ハク"], ["せま.る"]),
        ("盛り上がる", "もりあがる", "to rouse / swell / rise / get excited", [], ["もりあ.がる"]),
    ],
    # Lesson 97[cite: 35]
    [
        ("迫害", "はくがい", "persecution", ["ハクガイ"], []),
        ("圧迫", "あっぱく", "pressure / coercion / oppression", ["アッパク"], []),
        ("踏む", "ふむ", "to step on / tread on / experience", ["トウ"], ["ふ.む", "ふ.まえる"]),
        ("踏切", "ふみきり", "railway crossing / level crossing", [], ["ふみきり"]),
        ("並み", "なみ", "average / medium / common / ordinary", ["ヘイ"], ["な.み"]),
    ],
    # Lesson 98[cite: 35]
    [
        ("討", "とう", "chastise / attack / defeat / destroy / conquer", ["トウ"], ["う.つ"]),
        ("聖", "せい", "holy / saint / sage / master / priest", ["セイ", "ショウ"], ["ひじり"]),
        ("聖書", "せいしょ", "Bible / scriptures", ["セイショ"], []),
        ("神聖", "しんせい", "holiness / sacredness / sanctity / dignity", ["シンセイ"], []),
        ("検討", "けんとう", "consideration / examination / investigation", ["ケントウ"], []),
    ],
    # Lesson 99[cite: 35]
    [
        ("典", "てん", "code / ceremony / law / rule", ["テン"], []),
        ("辞典", "じてん", "dictionary / lexicon", ["ジテン"], []),
        ("剣", "けん", "sabre / sword / blade / clock hand", ["ケン"], ["つるぎ"]),
        ("真剣", "しんけん", "serious / earnest", ["シンケン"], []),
        ("典型", "てんけい", "type / pattern / model / epitome", ["テンケイ"], []),
    ],
    # Lesson 100[cite: 35]
    [
        ("症", "しょう", "symptoms / illness", ["ショウ"], []),
        ("花粉症", "かふんしょう", "hay fever / pollen allergy", ["カフンショウ"], []),
        ("納める", "おさめる", "to dedicate / make an offering / pay / supply", ["ノウ", "ナッ", "ナン"], ["おさ.める", "おさ.まる"]),
        ("納まる", "おさまる", "to be obtained / end / settle into / fit into", ["ノウ", "ナッ"], ["おさ.まる"]),
        ("走行", "そうこう", "running a wheeled vehicle / traveling", ["ソウコウ"], []),
    ],
    # Lesson 101[cite: 36]
    [
        ("納入", "のうにゅう", "payment (of taxes, fees) / supply / delivery", ["ノウニュウ"], []),
        ("納得", "なっとく", "consent / assent / agreement / understanding", ["ナットク"], []),
        ("浜", "はま", "beach / seashore", ["ヒン"], ["はま"]),
        ("横浜", "よこはま", "Yokohama", [], ["よこはま"]),
        ("悲鳴", "ひめい", "shriek / scream", ["ヒメイ"], []),
    ],
    # Lesson 102[cite: 36]
    [
        ("郷", "きょう", "home town / village / native place / district", ["キョウ", "ゴウ"], ["さと"]),
        ("郷里", "きょうり", "birth-place / home town", ["キョウリ"], []),
        ("惑わす", "まどわす", "to baffle / bewilder / confuse / mislead", ["ワク"], ["まど.わす"]),
        ("迷惑", "めいわく", "trouble / bother / annoyance", ["メイワク"], []),
        ("女房", "にょうぼう", "wife", ["ニョウボウ"], []),
    ],
    # Lesson 103[cite: 36]
    [
        ("拠", "きょ", "foothold / based on / follow / therefore", ["キョ", "コ"], ["よ.る"]),
        ("奉", "ほう", "observance / offer / present / dedicate", ["ホウ", "ブ"], ["たてまつ.る"]),
        ("奉仕", "ほうし", "service / ministry / attendance / church work", ["ホウシ"], []),
        ("壊れる", "こわれる", "to be broken / break", ["カイ"], ["こわ.れる", "こわ.す"]),
        ("証拠", "しょうこ", "evidence / proof", ["ショウコ"], []),
    ],
    # Lesson 104[cite: 36]
    [
        ("利益", "りえき", "profit / gains / benefit / advantage", ["リエキ"], []),
        ("収益", "しゅうえき", "earnings / proceeds / returns / revenue", ["シュウエキ"], []),
        ("有益", "ゆうえき", "beneficial / profitable / useful / instructive", ["ユウエキ"], []),
        ("句", "く", "phrase / clause / sentence / passage / haiku", ["ク"], []),
        ("益", "えき", "benefit / gain / profit / advantage", ["エキ", "ヤク"], ["ま.す"]),
    ],
    # Lesson 105[cite: 36]
    [
        ("属する", "ぞくする", "to belong to / come under / be affiliated with", ["ゾク"], ["ぞく.する"]),
        ("付属", "ふぞく", "attached / belonging / affiliated / annexed", ["フゾク"], []),
        ("金属", "きんぞく", "metal", ["キンゾク"], []),
        ("所属", "しょぞく", "belonging to (a group, organization, etc.)", ["ショゾク"], []),
        ("益々", "ますます", "increasingly / more and more", ["エキ"], ["ますます"]),
    ],
    # Lesson 106[cite: 36]
    [
        ("功", "こう", "achievement / merits / success / honor / credit", ["コウ", "ク"], ["いさお"]),
        ("成功", "せいこう", "success / achievement", ["セイコウ"], []),
        ("賀", "が", "congratulations / joy", ["ガ"], []),
        ("年賀状", "ねんがじょう", "New Year's card", ["ネンガジョウ"], []),
        ("破壊", "はかい", "destruction / disruption / demolition", ["ハカイ"], []),
    ],
    # Lesson 107[cite: 36]
    [
        ("堀", "ほり", "ditch / moat / canal", ["クツ"], ["ほり"]),
        ("泣く", "なく", "to cry / weep / sob / howl", ["キュウ"], ["な.く"]),
        ("記憶", "きおく", "memory / recollection / remembrance", ["キオク"], []),
        ("記憶力", "きおくりょく", "memory (power of retention)", ["キオクリョク"], []),
        ("憶", "おく", "recollection / think / remember", ["オク"], []),
    ],
    # Lesson 108[cite: 36]
    [
        ("幹", "みき", "tree trunk / main part", ["カン"], ["みき"]),
        ("新幹線", "しんかんせん", "Shinkansen / bullet train", ["シンカンセン"], []),
        ("露", "つゆ", "dew / tears / expose / Russia", ["ロ", "ロウ"], ["つゆ"]),
        ("暴露", "ばくろ", "disclosure / exposure / revelation", ["バクロ"], []),
        ("根拠", "こんきょ", "basis / grounds / foundation / authority", ["コンキョ"], []),
    ],
    # Lesson 109[cite: 36]
    [
        ("露骨", "ろこつ", "frank / blunt / plain / outspoken / undisguised", ["ロコツ"], []),
        ("矢", "や", "arrow", ["シ"], ["や"]),
        ("矢印", "やじるし", "directing arrow", [], ["やじるし"]),
        ("至る", "いたる", "to arrive at (e.g. a decision) / reach / attain", ["シ"], ["いた.る"]),
        ("矢っ張り", "やっぱり", "as expected / still / after all", [], ["やっぱり"]),
    ],
    # Lesson 110[cite: 36]
    [
        ("至って", "いたって", "very much / exceedingly / extremely", ["シ"], ["いた.って"]),
        ("至急", "しきゅう", "urgent / pressing / immediate", ["シキュウ"], []),
        ("握る", "にぎる", "to clasp / grasp / grip / clutch / make (sushi)", ["アク"], ["にぎ.る"]),
        ("握手", "あくしゅ", "handshake", ["アクシュ"], []),
        ("寄与", "きよ", "contribution / service", ["キヨ"], []),
    ],
    # Lesson 111[cite: 36]
    [
        ("儀", "ぎ", "ceremony / rule / affair / case / a matter", ["ギ"], []),
        ("礼儀", "れいぎ", "manners / courtesy / etiquette", ["レイギ"], []),
        ("行儀", "ぎょうぎ", "manners / behavior / deportment", ["ギョウギ"], []),
        ("襲う", "おそう", "to attack / assail / make an assault / succeed", ["シュウ"], ["おそ.う"]),
        ("告白", "こくはく", "confession / acknowledgement / profession of love", ["コクハク"], []),
    ],
    # Lesson 112[cite: 36]
    [
        ("徴", "ちょう", "indications / sign / omen / symptom / collect", ["チョウ"], ["しるし"]),
        ("特徴", "とくちょう", "feature / trait / characteristic / peculiarity", ["トクチョウ"], []),
        ("包丁", "ほうちょう", "kitchen knife / carving knife", ["ホウチョウ"], []),
        ("救う", "すくう", "to rescue from / help out of / save", ["キュウ"], ["すく.う"]),
        ("丁", "ちょう", "street / ward / town / counter for guns, tools", ["チョウ", "テイ"], ["ひのと"]),
    ],
    # Lesson 113[cite: 37]
    [
        ("救急車", "きゅうきゅうしゃ", "ambulance", ["キュウキュウシャ"], []),
        ("陰", "かげ", "shade / shadow / other side / back / background", ["イン"], ["かげ", "かげ.る"]),
        ("陰気", "いんき", "gloom / melancholy / dismal / somber", ["インキ"], []),
        ("日陰", "ひかげ", "shadow / shade", [], ["ひかげ"]),
        ("救済", "きゅうさい", "relief / aid / help / rescue / salvation", ["キュウサイ"], []),
    ],
    # Lesson 114[cite: 37]
    [
        ("繰る", "くる", "to reel / wind / spin (thread) / turn (pages)", ["ソウ"], ["く.る"]),
        ("繰り返す", "くりかえす", "to repeat / to do something over again", [], ["くりかえ.す"]),
        ("引っ繰り返す", "ひっくりかえす", "to turn over / overturn / knock over / upset", [], ["ひっくりかえ.す"]),
        ("引っ繰り返る", "ひっくりかえる", "to be overturned / be upset / topple over", [], ["ひっくりかえ.る"]),
        ("帯びる", "おびる", "to wear / carry / be entrusted with / have a trace of", ["タイ"], ["お.びる"]),
    ],
    # Lesson 115[cite: 37]
    [
        ("操る", "あやつる", "to manipulate / operate / handle / pull strings", ["ソウ"], ["あやつ.る", "みさお"]),
        ("操作", "そうさ", "operation / management / handling / manipulation", ["ソウサ"], []),
        ("体操", "たいそう", "gymnastics / physical exercises / calisthenics", ["タイソウ"], []),
        ("新体操", "しんたいそう", "rhythmic gymnastics", ["シンタイソウ"], []),
        ("周波", "しゅうは", "frequency (of waves)", ["シュウハ"], []),
    ],
    # Lesson 116[cite: 37]
    [
        ("騒ぐ", "さわぐ", "to make noise / make racket / be noisy / clamor", ["ソウ"], ["さわ.ぐ"]),
        ("己", "おのれ", "oneself", ["コ", "キ"], ["おのれ", "つちのと"]),
        ("鬼", "おに", "ogre / demon / spirit of a deceased person", ["キ"], ["おに"]),
        ("魔", "ま", "witch / demon / evil spirit", ["マ"], []),
        ("自己", "じこ", "self / oneself", ["ジコ"], []),
    ],
    # Lesson 117[cite: 37]
    [
        ("悪魔", "あくま", "devil / demon / fiend / Satan", ["アクマ"], []),
        ("誤魔化す", "ごまかす", "to deceive / falsify / cheat / gloss over", [], ["ごまか.す"]),
        ("撮る", "とる", "to take (a photo) / record (video, audio, etc.)", ["サツ"], ["と.る"]),
        ("撮影", "さつえい", "photography (still or motion) / shooting / filming", ["サツエイ"], []),
        ("衣装", "いしょう", "clothing / costume / outfit / garment / dress", ["イショウ"], []),
    ],
    # Lesson 118[cite: 37]
    [
        ("携わる", "たずさわる", "to engage in / participate in / take part in", ["ケイ"], ["たずさわ.る", "たずさ.える"]),
        ("携帯", "けいたい", "carrying (on one's person or in the hand) / mobile phone", ["ケイタイ"], []),
        ("携帯電話", "けいたいでんわ", "mobile telephone / cell phone", ["ケイタイデンワ"], []),
        ("隣", "となり", "neighbor / next to", ["リン"], ["とな.る", "となり"]),
        ("一見", "いっけん", "look / glimpse / glance / apparently / first meeting", ["イッケン"], []),
    ],
    # Lesson 119[cite: 37]
    [
        ("宣", "せん", "proclaim / say / announce", ["セン"], ["のたま.う"]),
        ("宣伝", "せんでん", "publicity / advertisement / advertising / propaganda", ["センデン"], []),
        ("遣", "けん", "dispatch / send / give / donate / do / undertake", ["ケン"], ["つか.う", "つか.わす"]),
        ("遣い", "つかい", "errand / mission / going as envoy / messenger", ["ケン"], ["つか.い"]),
        ("派遣", "はけん", "dispatch / deployment / sending", ["ハケン"], []),
    ],
    # Lesson 120[cite: 37]
    [
        ("小遣い", "こづかい", "personal expenses / pocket money / allowance", [], ["こづかい"]),
        ("言葉遣い", "ことばづかい", "speech / expression / wording / language", [], ["ことばづかい"]),
        ("訴え", "うったえ", "lawsuit / complaint", ["ソ"], ["うった.え"]),
        ("訴える", "うったえる", "to raise / bring to (someone's attention) / appeal to / sue", ["ソ"], ["うった.える"]),
        ("弾", "たま", "bullet / shot / shell", ["ダン"], ["たま"]),
    ],
    # Lesson 121[cite: 37]
    [
        ("茂る", "しげる", "to grow thickly / be in full leaf / be overgrown", ["モ"], ["しげ.る"]),
        ("お釣り", "おつり", "change (for a purchase)", [], ["おつり"]),
        ("誘い", "さそい", "invitation / temptation / enticement", ["ユウ"], ["さそ.い"]),
        ("誘う", "さそう", "to invite / ask (someone to do) / call (for) / tempt", ["ユウ"], ["さそ.う"]),
        ("楽器", "がっき", "musical instrument", ["ガッキ"], []),
    ],
    # Lesson 122[cite: 37]
    [
        ("核", "かく", "nucleus / core / kernel", ["カク"], []),
        ("哲", "てつ", "philosophy / clear", ["テツ"], ["あき.らか"]),
        ("哲学", "てつがく", "philosophy", ["テツガク"], []),
        ("憲", "けん", "constitution / law", ["ケン"], []),
        ("怒鳴る", "どなる", "to shout (in anger) / yell", [], ["どな.る"]),
    ],
    # Lesson 123[cite: 37]
    [
        ("豪華", "ごうか", "wonderful / gorgeous / splendor / pomp / extravagance", ["ゴウカ"], []),
        ("富豪", "ふごう", "wealthy person / millionaire", ["フゴウ"], []),
        ("締める", "しめる", "to tie / fasten / tighten / wear (necktie, belt)", ["テイ"], ["し.める", "し.まる"]),
        ("締め切り", "しめきり", "closing / cut-off / end / deadline / Closed", [], ["しめきり"]),
        ("取締り", "とりしまり", "control / management / supervision / crackdown", [], ["とりしまり"]),
    ],
    # Lesson 124[cite: 37]
    [
        ("締め切る", "しめきる", "to close up / shut up / cut off / end", [], ["しめき.る"]),
        ("鹿", "しか", "deer / cervid", ["ロク"], ["しか", "か"]),
        ("就く", "つく", "to take (seat, position, course, office, etc.)", ["シュウ", "ジュ"], ["つ.く", "つ.ける"]),
        ("滅びる", "ほろびる", "to go to ruin / go under / fall / be destroyed / die out", ["メツ"], ["ほろ.びる", "ほろ.ぼす"]),
        ("馬鹿", "ばか", "idiot / moron / fool / trivial matter / absurdity", ["バカ"], []),
    ],
    # Lesson 125[cite: 37]
    [
        ("滅ぼす", "ほろぼす", "to destroy / overthrow / wreck / ruin", ["メツ"], ["ほろ.ぼす"]),
        ("滅多に", "めったに", "rarely (with neg. verb) / seldom", ["メッタ"], []),
        ("仰ぐ", "あおぐ", "to look up (at) / respect / revere / ask for", ["ギョウ", "コウ"], ["あお.ぐ", "おお.せ"]),
        ("仰っしゃる", "おっしゃる", "to say / speak / tell / talk (honorific)", [], ["おっしゃ.る"]),
        ("仰る", "おっしゃる", "to say / speak / tell / talk (honorific)", ["ギョウ"], ["おっしゃ.る"]),
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
    if not os.path.isdir(KANJIVG_DIR):
        raise FileNotFoundError(f"Could not find '{KANJIVG_DIR}'.")

    lessons = []
    item_counter = 1

    for l_idx, chunk in enumerate(N1_PART1_DATA):
        lesson_num = l_idx + 1
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

    with open(PART1_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(lessons, f, ensure_ascii=False)

    print(f"Part 1 complete! Saved Lessons 1-125 ({item_counter - 1} items) to {PART1_JSON_PATH}.")


if __name__ == "__main__":
    main()