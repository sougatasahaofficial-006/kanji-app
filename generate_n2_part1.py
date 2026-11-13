import os
import json
import xml.etree.ElementTree as ET

KANJIVG_DIR = "kanjivg-data"
PART1_JSON_PATH = "n2_part1.json"

N2_PART1_DATA = [
    # Lesson 1[cite: 34]
    [
        ("軍", "ぐん", "army / troops", ["グン"], []),
        ("兵", "へい", "soldier / troops", ["ヘイ", "ヒョウ"], ["つわもの"]),
        ("島", "しま", "island", ["トウ"], ["しま"]),
        ("広島", "ひろしま", "Hiroshima", [], ["ひろしま"]),
        ("年度", "ねんど", "fiscal year / school year", ["ネンド"], []),
    ],
    # Lesson 2[cite: 34]
    [
        ("村", "むら", "village", ["ソン"], ["むら"]),
        ("戸", "と", "door / household", ["コ"], ["と"]),
        ("感ずる", "かんずる", "to feel / sense", ["カン"], ["かん.ずる"]),
        ("因みに", "ちなみに", "by the way / incidentally", ["イン"], ["ちな.みに"]),
    ],
    # Lesson 3[cite: 34]
    [
        ("神戸", "こうべ", "Kobe", [], ["こうべ"]),
        ("武", "ぶ", "warrior / military", ["ブ", "ム"], ["たけ"]),
        ("城", "しろ", "castle", ["ジョウ"], ["しろ"]),
        ("糸", "いと", "thread / yarn", ["シ"], ["いと"]),
    ],
    # Lesson 4[cite: 34]
    [
        ("総", "そう", "whole / total / general", ["ソウ"], ["す.べて"]),
        ("団", "だん", "group / corps / party", ["ダン", "トン"], []),
        ("団体", "だんたい", "organization / group", ["ダンタイ"], []),
        ("団体旅行", "だんたいりょこう", "group tour", ["ダンタイリョコウ"], []),
    ],
    # Lesson 5[cite: 34]
    [
        ("線", "せん", "line / wire / track", ["セン"], []),
        ("線路", "せんろ", "railway track", ["センロ"], []),
        ("番線", "ばんせん", "track number / platform", ["バンセン"], []),
        ("設ける", "もうける", "to establish / set up", ["セツ"], ["もう.ける"]),
    ],
    # Lesson 6[cite: 34]
    [
        ("設備", "せつび", "equipment / facilities", ["セツビ"], []),
        ("勢い", "いきおい", "force / vigor / momentum", ["セイ"], ["いきお.い"]),
        ("大勢", "おおぜい", "crowd / great number of people", ["タイセイ"], ["おおぜい"]),
        ("党", "とう", "political party / faction", ["トウ"], []),
        ("重ねる", "かさねる", "to pile up / repeat", ["ジュウ", "チョウ"], ["かさ.ねる", "かさ.なる"]),
    ],
    # Lesson 7[cite: 34]
    [
        ("政党", "せいとう", "political party", ["セイトウ"], []),
        ("史", "し", "history / chronicles", ["シ"], []),
        ("営む", "いとなむ", "to run (a business) / carry on", ["エイ"], ["いとな.む"]),
        ("営業", "えいぎょう", "business / sales / operations", ["エイギョウ"], []),
        ("相互", "そうご", "mutual / reciprocal", ["ソウゴ"], []),
    ],
    # Lesson 8[cite: 34]
    [
        ("経営", "けいえい", "management / administration", ["ケイエイ"], []),
        ("府", "ふ", "urban prefecture / government office", ["フ"], []),
        ("政府", "せいふ", "government", ["セイフ"], []),
        ("巻く", "まく", "to wind / roll / wrap", ["カン"], ["ま.く"]),
        ("市町村", "しちょうそん", "municipalities (cities, towns, villages)", ["シチョウソン"], []),
    ],
    # Lesson 9[cite: 34]
    [
        ("介して", "かいして", "through / via", ["カイ"], []),
        ("臣", "しん", "retainer / minister / subject", ["シン", "ジン"], []),
        ("大臣", "だいじん", "cabinet minister", ["ダイジン"], []),
        ("総理大臣", "そうりだいじん", "Prime Minister", ["ソウリダイジン"], []),
        ("工夫", "くふう", "devising / ingenuity", ["クフウ"], []),
    ],
    # Lesson 10[cite: 34]
    [
        ("蔵", "くら", "warehouse / storehouse", ["ゾウ"], ["くら"]),
        ("造る", "つくる", "to make / manufacture / build", ["ゾウ"], ["つく.る"]),
        ("造船", "ぞうせん", "shipbuilding", ["ゾウセン"], []),
        ("構造", "こうぞう", "structure / construction", ["コウゾウ"], []),
        ("留まる", "とどまる", "to remain / stay", ["リュウ"], ["とど.まる", "と.まる"]),
    ],
    # Lesson 11[cite: 34]
    [
        ("人造", "じんぞう", "synthetic / artificial / man-made", ["ジンゾウ"], []),
        ("根", "ね", "root", ["コン"], ["ね"]),
        ("屋根", "やね", "roof", [], ["やね"]),
        ("お寺", "おてら", "Buddhist temple", ["ジ"], ["てら"]),
        ("有り難い", "ありがたい", "grateful / thankful", [], ["ありがた.い"]),
    ],
    # Lesson 12[cite: 34]
    [
        ("査", "さ", "investigate / inspect", ["サ"], []),
        ("調査", "ちょうさ", "investigation / survey", ["チョウサ"], []),
        ("将", "しょう", "commander / general / future", ["ショウ"], []),
        ("将来", "しょうらい", "future / prospects", ["ショウライ"], []),
        ("勝負", "しょうぶ", "victory or defeat / match", ["ショウブ"], []),
    ],
    # Lesson 13[cite: 34]
    [
        ("改めて", "あらためて", "another time / again / formally", ["カイ"], ["あらた.めて"]),
        ("改める", "あらためる", "to change / reform / revise", ["カイ"], ["あらた.める"]),
        ("改行", "かいぎょう", "line break / new paragraph", ["カイギョウ"], []),
        ("県", "けん", "prefecture", ["ケン"], []),
    ],
    # Lesson 14[cite: 34]
    [
        ("県立", "けんりつ", "prefectural", ["ケンリツ"], []),
        ("泉", "いずみ", "spring / fountain", ["セン"], ["いずみ"]),
        ("像", "ぞう", "statue / image / figure", ["ゾウ"], []),
        ("画像", "がぞう", "image / picture", ["ガゾウ"], []),
        ("給与", "きゅうよ", "pay / salary / wages", ["キュウヨ"], []),
    ],
    # Lesson 15[cite: 34]
    [
        ("映像", "えいぞう", "image / video / footage", ["エイゾウ"], []),
        ("想像", "そうぞう", "imagination", ["ソウゾウ"], []),
        ("想像力", "そうぞうりょく", "imaginative power", ["ソウゾウリョク"], []),
        ("細い", "ほそい", "thin / slender / narrow", ["サイ"], ["ほそ.い", "こま.かい"]),
        ("次ぐ", "つぐ", "to rank next to / follow", ["ジ"], ["つ.ぐ"]),
    ],
    # Lesson 16[cite: 34]
    [
        ("細め", "ほそめ", "somewhat narrow / slim", ["サイ"], ["ほそ.め"]),
        ("細かい", "こまかい", "small / fine / detailed", ["サイ"], ["こま.かい"]),
        ("細かいお金", "こまかいおかね", "small change", [], ["こまかいおかね"]),
        ("谷", "たに", "valley", ["コク"], ["たに"]),
        ("組合せ", "くみあわせ", "combination", [], ["くみあわせ"]),
    ],
    # Lesson 17[cite: 34]
    [
        ("奥さん", "おくさん", "wife (polite)", ["オウ"], ["おく"]),
        ("再び", "ふたたび", "again / once more", ["サイ", "サ"], ["ふたた.び"]),
        ("再来週", "さらいしゅう", "week after next", ["サライシュウ"], []),
        ("再来月", "さらいげつ", "month after next", ["サライゲツ"], []),
        ("有無", "うむ", "existence or nonexistence", ["ウム"], []),
    ],
    # Lesson 18[cite: 34]
    [
        ("再来年", "さらいねん", "year after next", ["サライネン"], []),
        ("再利用", "さいりよう", "reuse / recycling", ["サイリヨウ"], []),
        ("再放送", "さいほうそう", "rebroadcast / rerun", ["サイホウソウ"], []),
        ("お皿", "おさら", "plate / dish", ["ベイ"], ["さら"]),
        ("半島", "はんとう", "peninsula", ["ハントウ"], []),
    ],
    # Lesson 19[cite: 34]
    [
        ("血", "ち", "blood", ["ケツ"], ["ち"]),
        ("竹", "たけ", "bamboo", ["チク"], ["たけ"]),
        ("算", "さん", "calculate / divining", ["サン"], []),
        ("算数", "さんすう", "arithmetic", ["サンスウ"], []),
        ("貸付", "かしつけ", "loaning / lending", [], ["かしつけ"]),
    ],
    # Lesson 20[cite: 34]
    [
        ("計算", "けいさん", "calculation", ["ケイサン"], []),
        ("精算", "せいさん", "fare adjustment / settlement", ["セイサン"], []),
        ("予算", "よさん", "budget / estimate", ["ヨサン"], []),
        ("足し算", "たしざん", "addition", [], ["たしざん"]),
        ("人参", "にんじん", "carrot", ["ニンジン"], []),
    ],
    # Lesson 21[cite: 35]
    [
        ("割り算", "わりざん", "division (math)", [], ["わりざん"]),
        ("引き算", "ひきざん", "subtraction", [], ["ひきざん"]),
        ("象", "ぞう", "elephant / phenomenon", ["ショウ", "ゾウ"], []),
        ("対象", "たいしょう", "target / object / subject", ["タイショウ"], []),
        ("申立", "もうしたて", "statement / application", [], ["もうしたて"]),
    ],
    # Lesson 22[cite: 35]
    [
        ("清む", "すむ", "to become clear (water/air)", ["セイ", "ショウ"], ["きよ.い", "す.む"]),
        ("清い", "きよい", "clear / pure / noble", ["セイ"], ["きよ.い"]),
        ("清書", "せいしょ", "clean copy / fair copy", ["セイショ"], []),
        ("技", "わざ", "technique / art / skill", ["ギ"], ["わざ"]),
        ("東西", "とうざい", "east and west", ["トウザイ"], []),
    ],
    # Lesson 23[cite: 35]
    [
        ("技術", "ぎじゅつ", "technology / engineering / skill", ["ギジュツ"], []),
        ("州", "しゅう", "state / province / continent", ["シュウ"], ["す"]),
        ("貝", "かい", "shellfish / shell", ["バイ"], ["かい"]),
        ("寝室", "しんしつ", "bedroom", ["シンシツ"], []),
        ("仕草", "しぐさ", "gesture / behavior", [], ["しぐさ"]),
    ],
    # Lesson 24[cite: 35]
    [
        ("領", "りょう", "territory / jurisdiction", ["リョウ"], []),
        ("領収書", "りょうしゅうしょ", "receipt", ["リョウシュウショ"], []),
        ("橋", "はし", "bridge", ["キョウ"], ["はし"]),
        ("歩道橋", "ほどうきょう", "pedestrian overpass", ["ホドウキョウ"], []),
        ("関西", "かんさい", "Kansai region", ["カンサイ"], []),
    ],
    # Lesson 25[cite: 35]
    [
        ("芸", "げい", "art / craft / performance", ["ゲイ"], []),
        ("芸術", "げいじゅつ", "fine arts / art", ["ゲイジュツ"], []),
        ("型", "かた", "mold / type / model", ["ケイ"], ["かた"]),
        ("髪型", "かみがた", "hairstyle", [], ["かみがた"]),
        ("手形", "てがた", "promissory note / handprint", [], ["てがた"]),
    ],
    # Lesson 26[cite: 35]
    [
        ("大型", "おおがた", "large-sized / large-scale", ["オオガタ"], []),
        ("小型", "こがた", "small-sized / compact", ["コガタ"], []),
        ("大型連休", "おおがたれんきゅう", "long holiday period (Golden Week)", [], ["おおがたれんきゅう"]),
        ("香り", "かおり", "aroma / fragrance / scent", ["コウ", "キョウ"], ["かお.り", "か"]),
        ("香港", "ホンコン", "Hong Kong", ["ホンコン"], []),
    ],
    # Lesson 27[cite: 35]
    [
        ("香水", "こうすい", "perfume", ["コウスイ"], []),
        ("里", "さと", "hometown / village", ["リ"], ["さと"]),
        ("量", "りょう", "quantity / amount / volume", ["リョウ"], ["はか.る"]),
        ("久しぶり", "ひさしぶり", "after a long time", ["キュウ"], ["ひさ.しい"]),
        ("南北", "なんぼく", "north and south", ["ナンボク"], []),
    ],
    # Lesson 28[cite: 35]
    [
        ("境", "さかい", "border / boundary", ["キョウ", "ケイ"], ["さかい"]),
        ("国境", "こっきょう", "national border", ["コッキョウ"], []),
        ("境界", "きょうかい", "boundary / border", ["キョウカイ"], []),
        ("比べる", "くらべる", "to compare", ["ヒ"], ["くら.べる"]),
        ("冷める", "さめる", "to cool down / lose interest", ["レイ"], ["さ.める"]),
    ],
    # Lesson 29[cite: 35]
    [
        ("階", "かい", "floor / story / stairs", ["カイ"], []),
        ("階段", "かいだん", "stairs / staircase", ["カイダン"], []),
        ("何階", "なんがい", "what floor", ["ナンガイ"], []),
        ("区", "く", "ward / district / section", ["ク"], []),
        ("彼方", "かなた", "beyond / over there", [], ["かなた"]),
    ],
    # Lesson 30[cite: 35]
    [
        ("区別", "くべつ", "distinction / differentiation", ["クベツ"], []),
        ("皮", "かわ", "skin / peel / leather", ["ヒ"], ["かわ"]),
        ("皮ふ", "ひふ", "skin", ["ヒフ"], []),
        ("波", "なみ", "wave", ["ハ"], ["なみ"]),
        ("電波", "でんぱ", "radio wave / reception", ["デンパ"], []),
    ],
    # Lesson 31[cite: 35]
    [
        ("移る", "うつる", "to move / transfer / shift", ["イ"], ["うつ.る", "うつ.す"]),
        ("移す", "うつす", "to move / transfer / infect", ["イ"], ["うつ.す"]),
        ("移転", "いてん", "relocation / moving", ["イテン"], []),
        ("域", "いき", "region / range / limits", ["イキ"], []),
        ("力強い", "ちからづよい", "powerful / reassuring", [], ["ちからづよ.い"]),
    ],
    # Lesson 32[cite: 35]
    [
        ("地域", "ちいき", "area / region", ["チイキ"], []),
        ("周り", "まわり", "surroundings / circumference", ["シュウ"], ["まわ.り"]),
        ("接する", "せっする", "to touch / contact / adjoin", ["セツ"], ["せ.する", "つ.ぐ"]),
        ("面接", "めんせつ", "interview", ["メンセツ"], []),
        ("強引", "ごういん", "forcible / pushy / assertive", ["ゴウイン"], []),
    ],
    # Lesson 33[cite: 35]
    [
        ("直接", "ちょくせつ", "direct / directly", ["チョクセツ"], []),
        ("鉄", "てつ", "iron / steel", ["テツ"], []),
        ("私鉄", "してつ", "private railway", ["シテツ"], []),
        ("地下鉄", "ちかてつ", "subway / metro", ["チカテツ"], []),
        ("寺院", "じいん", "Buddhist temple", ["ジイン"], []),
    ],
    # Lesson 34[cite: 35]
    [
        ("この頃", "このごろ", "these days / recently", [], ["このごろ"]),
        ("材", "ざい", "lumber / material / talent", ["ザイ"], []),
        ("材料", "ざいりょう", "ingredients / material", ["ザイリョウ"], []),
        ("億", "おく", "hundred million", ["オク"], []),
        ("頃", "ころ", "around / about (time)", ["ケイ", "キョウ"], ["ころ"]),
    ],
    # Lesson 35[cite: 35]
    [
        ("個人", "こじん", "individual / private person", ["コジン"], []),
        ("個性", "こせい", "individuality / personality", ["コセイ"], []),
        ("何個", "なんこ", "how many (small objects)", ["ナンコ"], []),
        ("一個", "いっこ", "one (small object)", ["イッコ"], []),
        ("物語る", "ものがたる", "to tell / indicate", [], ["ものがた.る"]),
    ],
    # Lesson 36[cite: 35]
    [
        ("二個", "にこ", "two (small objects)", ["ニコ"], []),
        ("三個", "さんこ", "three (small objects)", ["サンコ"], []),
        ("六個", "ろっこ", "six (small objects)", ["ロッコ"], []),
        ("七個", "ななこ", "seven (small objects)", ["ナナコ"], []),
        ("背骨", "せぼね", "spine / backbone", [], ["せぼね"]),
    ],
    # Lesson 37[cite: 35]
    [
        ("八個", "はっこ", "eight (small objects)", ["ハッコ"], []),
        ("九個", "きゅうこ", "nine (small objects)", ["キュウコ"], []),
        ("十個", "じゅっこ", "ten (small objects)", ["ジュッコ"], []),
        ("四個", "よんこ", "four (small objects)", ["ヨンコ"], []),
        ("危うい", "あやうい", "dangerous / critical", ["キ"], ["あや.うい"]),
    ],
    # Lesson 38[cite: 35]
    [
        ("五個", "ごこ", "five (small objects)", ["ゴコ"], []),
        ("個人的", "こじんてき", "personal / individual", ["コジンテキ"], []),
        ("個性的", "こせいてき", "unique / individualistic", ["コセイテキ"], []),
        ("合戦", "かっせん", "battle / military engagement", ["カッセン"], []),
        ("境内", "けいだい", "shrine/temple precincts", ["ケイダイ"], []),
    ],
    # Lesson 39[cite: 35]
    [
        ("個人情報", "こじんじょうほう", "personal information", ["コジンジョウホウ"], []),
        ("協", "きょう", "cooperate", ["キョウ"], []),
        ("協力", "きょうりょく", "cooperation / collaboration", ["キョウリョク"], []),
        ("各", "かく", "each / every", ["カク"], ["おのおの"]),
        ("各国", "かっこく", "each country / various nations", ["カッコク"], []),
    ],
    # Lesson 40[cite: 35]
    [
        ("各駅", "かくえき", "every station", ["カクエキ"], []),
        ("帯", "おび", "sash / belt / zone", ["タイ"], ["お.びる", "おび"]),
        ("熱帯", "ねったい", "tropics", ["ネッタイ"], []),
        ("温帯", "おんたい", "temperate zone", ["オンタイ"], []),
        ("各々", "おのおの", "each / respectively", ["カク"], ["おのおの"]),
    ],
    # Lesson 41[cite: 36]
    [
        ("寒帯", "かんたい", "frigid zone / arctic zone", ["カンタイ"], []),
        ("歴", "れき", "curriculum / continuation", ["レキ"], []),
        ("歴史", "れきし", "history", ["レキシ"], []),
        ("冊", "さつ", "counter for books", ["サツ", "サク"], []),
        ("貸出", "かしだし", "lending / checkout", [], ["かしだし"]),
    ],
    # Lesson 42[cite: 36]
    [
        ("編む", "あむ", "to knit / braid / compile", ["ヘン"], ["あ.む"]),
        ("編集", "へんしゅう", "editing / compilation", ["ヘンシュウ"], []),
        ("編み物", "あみもの", "knitting / knitted goods", [], ["あみもの"]),
        ("衣", "ころも", "garment / clothes / coating", ["イ"], ["ころも", "きぬ"]),
        ("教わる", "おそわる", "to be taught / learn from", ["キョウ"], ["おそ.わる"]),
    ],
    # Lesson 43[cite: 36]
    [
        ("衣服", "いふく", "clothes / garments", ["イフク"], []),
        ("衣食住", "いしょくじゅう", "food, clothing, and shelter", ["イショクジュウ"], []),
        ("裏", "うら", "back / reverse side / inside", ["リ"], ["うら"]),
        ("裏返し", "うらがえし", "inside out / upside down", [], ["うらがえし"]),
        ("打合せ", "うちあわせ", "business meeting / arrangement", [], ["うちあわせ"]),
    ],
    # Lesson 44[cite: 36]
    [
        ("裏返す", "うらがえす", "to turn inside out / flip over", [], ["うらがえ.す"]),
        ("装う", "よそおう", "to dress up / pretend", ["ソウ", "ショウ"], ["よそお.う"]),
        ("服装", "ふくそう", "attire / dress / clothing", ["フクソウ"], []),
        ("女将", "おかみ", "landlady / proprietress", [], ["おかみ"]),
        ("格子", "こうし", "lattice / grid", ["コウシ"], []),
    ],
    # Lesson 45[cite: 36]
    [
        ("省く", "はぶく", "to omit / save / cut down", ["セイ", "ショウ"], ["はぶ.く", "かえり.みる"]),
        ("税", "ぜい", "tax / duty", ["ゼイ"], []),
        ("税込", "ぜいこみ", "tax included", ["ゼイコミ"], []),
        ("税金", "ぜいきん", "tax / duty", ["ゼイキン"], []),
        ("反省", "はんせい", "reflection / self-examination", ["ハンセイ"], []),
    ],
    # Lesson 46[cite: 36]
    [
        ("税別", "ぜいべつ", "tax excluded", ["ゼイベツ"], []),
        ("競る", "せる", "to compete / bid", ["キョウ", "ケイ"], ["きそ.う", "せ.る"]),
        ("競争", "きょうそう", "competition / rivalry", ["キョウソウ"], []),
        ("競争相手", "きょうそうあいて", "competitor / rival", ["キョウソウアイテ"], []),
        ("競馬", "けいば", "horse racing", ["ケイバ"], []),
    ],
    # Lesson 47[cite: 36]
    [
        ("囲む", "かこむ", "to surround / encircle", ["イ"], ["かこ.む", "かこ.う"]),
        ("辺", "へん", "area / vicinity / side", ["ヘン"], ["あた.り", "べ"]),
        ("辺り", "あたり", "neighborhood / vicinity", ["ヘン"], ["あた.り"]),
        ("周辺", "しゅうへん", "circumference / outskirts", ["シュウヘン"], []),
        ("競う", "きそう", "to compete / vie", ["キョウ"], ["きそ.う"]),
    ],
    # Lesson 48[cite: 36]
    [
        ("河", "かわ", "river / stream", ["カ"], ["かわ"]),
        ("運河", "うんが", "canal / waterway", ["ウンガ"], []),
        ("極", "きょく", "pole / extreme / limit", ["キョク", "ゴク"], ["きわ.める"]),
        ("北極", "ほっきょく", "North Pole", ["ホッキョク"], []),
        ("足取り", "あしどり", "gait / pace / movements", [], ["あしどり"]),
    ],
    # Lesson 49[cite: 36]
    [
        ("南極", "なんきょく", "South Pole / Antarctica", ["ナンキョク"], []),
        ("積極的", "せっきょくてき", "positive / proactive / active", ["セッキョクテキ"], []),
        ("消極的", "しょうきょくてき", "passive / negative", ["ショウキョクテキ"], []),
        ("防ぐ", "ふせぐ", "to defend against / prevent", ["ボウ"], ["ふせ.ぐ"]),
        ("神道", "しんとう", "Shintoism", ["シントウ"], []),
    ],
    # Lesson 50[cite: 36]
    [
        ("低い", "ひくい", "low / short", ["テイ"], ["ひく.い", "ひく.める"]),
        ("最低", "さいてい", "lowest / minimum / worst", ["サイテイ"], []),
        ("林", "はやし", "woods / grove / forest", ["リン"], ["はやし"]),
        ("導く", "みちびく", "to guide / lead", ["ドウ"], ["みちび.く"]),
        ("小林", "こばやし", "Kobayashi (surname)", [], ["こばやし"]),
    ],
    # Lesson 51[cite: 37]
    [
        ("指導", "しどう", "guidance / leadership / coaching", ["シドウ"], []),
        ("森", "もり", "forest", ["シン"], ["もり"]),
        ("森林", "しんりん", "forest / woods", ["シンリン"], []),
        ("丸", "まる", "circle / whole / full", ["ガン"], ["まる", "まる.い"]),
        ("薬局", "やっきょく", "pharmacy / drugstore", ["ヤッキョク"], []),
    ],
    # Lesson 52[cite: 37]
    [
        ("胸", "むね", "chest / breast / heart", ["キョウ"], ["むね", "むな-"]),
        ("陸", "りく", "land / shore", ["リク"], []),
        ("大陸", "たいりく", "continent", ["タイリク"], []),
        ("療", "りょう", "heal / cure", ["リョウ"], []),
        ("成り行き", "なりゆき", "course of events / outcome", [], ["なりゆき"]),
    ],
    # Lesson 53[cite: 37]
    [
        ("治療", "ちりょう", "medical treatment", ["チリョウ"], []),
        ("治療費", "ちりょうひ", "medical expenses", ["チリョウヒ"], []),
        ("諸", "しょ", "various / many / several", ["ショ"], []),
        ("管", "くだ", "pipe / tube", ["カン"], ["くだ"]),
        ("管理", "かんり", "management / control", ["カンリ"], []),
    ],
    # Lesson 54[cite: 37]
    [
        ("管理人", "かんりにん", "manager / caretaker / superintendent", ["カンリニン"], []),
        ("仲", "なか", "relation / relationship", ["チュウ"], ["なか"]),
        ("仲間", "なかま", "companion / fellow / colleague", [], ["なかま"]),
        ("仲直り", "なかなおり", "reconciliation / making up", [], ["なかなおり"]),
        ("諸々", "もろもろ", "various / all kinds of", ["ショ"], ["もろもろ"]),
    ],
    # Lesson 55[cite: 37]
    [
        ("仲良し", "なかよし", "close friend / bosom buddy", [], ["なかよし"]),
        ("遊び仲間", "あそびなかま", "playmate", [], ["あそびなかま"]),
        ("革", "かわ", "leather / reform", ["カク"], ["かわ"]),
        ("抱く", "いだく", "to harbor / embrace / hold", ["ホウ"], ["いだ.く"]),
        ("仲介", "ちゅうかい", "mediation / intermediary", ["チュウカイ"], []),
    ],
    # Lesson 56[cite: 37]
    [
        ("担当", "たんとう", "being in charge", ["タントウ"], []),
        ("担当者", "たんとうしゃ", "person in charge", ["タントウシャ"], []),
        ("効く", "きく", "to be effective / work", ["コウ"], ["き.く"]),
        ("有効期限", "ゆうこうきげん", "expiration date", ["ユウコウキゲン"], []),
        ("雑草", "ざっそう", "weed", ["ザッソウ"], []),
    ],
    # Lesson 57[cite: 37]
    [
        ("賞", "しょう", "prize / award", ["ショウ"], []),
        ("賞品", "しょうひん", "prize / trophy", ["ショウヒン"], []),
        ("賞金", "しょうきん", "prize money", ["ショウキン"], []),
        ("星", "ほし", "star / planet", ["セイ", "ショウ"], ["ほし"]),
        ("集う", "つどう", "to gather / assemble", ["シュウ"], ["つど.う"]),
    ],
    # Lesson 58[cite: 37]
    [
        ("復す", "ふくす", "to return to / restore", ["フク"], ["ふく.す"]),
        ("復習", "ふくしゅう", "review (of lessons)", ["フクシュウ"], []),
        ("回復", "かいふく", "recovery / restoration", ["カイフク"], []),
        ("片づけ", "かたづけ", "tidying up / cleaning up", [], ["かたづけ"]),
        ("日向", "ひなた", "sunny place", [], ["ひなた"]),
    ],
    # Lesson 59[cite: 37]
    [
        ("片道", "かたみち", "one-way (trip)", [], ["かたみち"]),
        ("片方", "かたほう", "one side / one of a pair", [], ["かたほう"]),
        ("片付く", "かたづく", "to be tidied up / settled", [], ["かたづ.く"]),
        ("片付ける", "かたづける", "to tidy up / put in order", [], ["かたづ.ける"]),
        ("引き金", "ひきがね", "trigger", [], ["ひきがね"]),
    ],
    # Lesson 60[cite: 37]
    [
        ("並ぶ", "ならぶ", "to line up / stand in a row", ["ヘイ"], ["なら.ぶ", "なら.べる"]),
        ("並べる", "ならべる", "to line up / arrange", ["ヘイ"], ["なら.べる"]),
        ("並", "なみ", "average / medium / ordinary", ["ヘイ"], ["なみ"]),
        ("温かい", "あたたかい", "warm / mild", ["オン"], ["あたた.かい", "あたた.める"]),
        ("並木", "なみき", "roadside tree / row of trees", [], ["なみき"]),
    ],
    # Lesson 61[cite: 37]
    [
        ("温める", "あたためる", "to warm / heat", ["オン"], ["あたため.る"]),
        ("温泉", "おんせん", "hot spring", ["オンセン"], []),
        ("気温", "きおん", "air temperature", ["キオン"], []),
        ("体温", "たいおん", "body temperature", ["タイオン"], []),
        ("青白い", "あおじろい", "pale / bluish-white", [], ["あおじろ.い"]),
    ],
    # Lesson 62[cite: 37]
    [
        ("体温計", "たいおんけい", "clinical thermometer", ["タイオンケイ"], []),
        ("温度計", "おんどけい", "thermometer", ["オンドケイ"], []),
        ("軽い", "かるい", "light / slight / easy", ["ケイ"], ["かる.い"]),
        ("手軽", "てがる", "easy / simple / handy", [], ["てがる"]),
        ("同居", "どうきょ", "living together / cohabitation", ["ドウキョ"], []),
    ],
    # Lesson 63[cite: 37]
    [
        ("気軽", "きがる", "cheerful / lighthearted / casual", [], ["きがる"]),
        ("口が軽い", "くちがかるい", "talkative / indiscreet", [], ["くちがかる.い"]),
        ("録", "ろく", "record / copy", ["ロク"], []),
        ("録画", "ろくが", "video recording", ["ロクガ"], []),
        ("最期", "さいご", "one's last moment / death", ["サイゴ"], []),
    ],
    # Lesson 64[cite: 37]
    [
        ("録音", "ろくおん", "audio recording", ["ロクオン"], []),
        ("腰", "こし", "lower back / waist / hip", ["ヨウ"], ["こし"]),
        ("腰掛ける", "こしかける", "to sit down", [], ["こしか.ける"]),
        ("著す", "あらわす", "to write / publish", ["チョ"], ["あらわ.す", "いちじる.しい"]),
        ("真似る", "まねる", "to imitate / mimic", [], ["まね.る"]),
    ],
    # Lesson 65[cite: 37]
    [
        ("著者", "ちょしゃ", "author / writer", ["チョシャ"], []),
        ("乱す", "みだす", "to disturb / disorder", ["ラン"], ["みだ.す", "みだ.れる"]),
        ("章", "しょう", "chapter / section / badge", ["ショウ"], []),
        ("文章", "ぶんしょう", "sentence / writing / text", ["ブンショウ"], []),
        ("神父", "しんぷ", "Catholic priest / father", ["シンプ"], []),
    ],
    # Lesson 66[cite: 37]
    [
        ("殿", "との", "lord / feudal lord / Mr.", ["デン", "テン"], ["との", "どの"]),
        ("布", "ぬの", "cloth / fabric", ["フ"], ["ぬの"]),
        ("財布", "さいふ", "wallet / purse", ["サイフ"], []),
        ("布団", "ふとん", "futon / bedding", ["フトン"], []),
        ("分布", "ぶんぷ", "distribution", ["ブンプ"], []),
    ],
    # Lesson 67[cite: 37]
    [
        ("座布団", "ざぶとん", "floor cushion", ["ザブトン"], []),
        ("角", "かど", "corner / angle / horn", ["カク"], ["かど", "つの"]),
        ("四角", "しかく", "square / quadrilateral", ["シカク"], []),
        ("三角", "さんかく", "triangle", ["サンカク"], []),
        ("方角", "ほうがく", "direction / compass point", ["ホウガク"], []),
    ],
    # Lesson 68[cite: 37]
    [
        ("三角形", "さんかっけい", "triangle (shape)", ["サンカッケイ"], []),
        ("仏", "ほとけ", "Buddha / merciful person", ["ブツ"], ["ほとけ"]),
        ("永い", "ながい", "long (time) / eternal", ["エイ"], ["なが.い"]),
        ("永久", "えいきゅう", "eternity / permanence", ["エイキュウ"], []),
        ("仏教", "ぶっきょう", "Buddhism", ["ブッキョウ"], []),
    ],
    # Lesson 69[cite: 37]
    [
        ("永遠", "えいえん", "eternity / immortality", ["エイエン"], []),
        ("誌", "し", "magazine / journal / records", ["シ"], []),
        ("雑誌", "ざっし", "magazine / periodical", ["ザッシ"], []),
        ("減る", "へる", "to decrease / diminish", ["ゲン"], ["へ.る", "へ.らす"]),
        ("風情", "ふぜい", "taste / elegance / charm", ["フゼイ"], []),
    ],
    # Lesson 70[cite: 37]
    [
        ("減らす", "へらす", "to reduce / decrease", ["ゲン"], ["へ.らす"]),
        ("減少", "げんしょう", "decrease / reduction", ["ゲンショウ"], []),
        ("いい加減", "いいかげん", "irresponsible / lukewarm / moderate", ["イイカゲン"], []),
        ("略す", "りゃくす", "to abbreviate / omit", ["リャク"], ["りゃく.す"]),
        ("今時", "いまどき", "nowadays / these days", [], ["いまどき"]),
    ],
    # Lesson 71[cite: 37]
    [
        ("省略", "しょうりゃく", "omission / abbreviation", ["ショウリャク"], []),
        ("準じる", "じゅんじる", "to conform to / correspond to", ["ジュン"], ["じゅん.じる"]),
        ("準備", "じゅんび", "preparation / arrangement", ["ジュンビ"], []),
        ("委ねる", "ゆだねる", "to entrust / devote oneself to", ["イ"], ["ゆだ.ねる"]),
        ("積立", "つみたて", "reserve / installment savings", [], ["つみたて"]),
    ],
    # Lesson 72[cite: 37]
    [
        ("委員", "いいん", "committee member", ["イイン"], []),
        ("令", "れい", "orders / command / decree", ["レイ"], []),
        ("命令", "めいれい", "order / command", ["メイレイ"], []),
        ("干す", "ほす", "to air / dry", ["カン"], ["ほ.す", "ひ.る"]),
        ("梅干", "うめぼし", "pickled plum", [], ["うめぼし"]),
    ],
    # Lesson 73[cite: 38]
    [
        ("刊", "かん", "publication / edition", ["カン"], []),
        ("週刊誌", "しゅうかんし", "weekly magazine", ["シュウカンシ"], []),
        ("月刊誌", "げっかんし", "monthly magazine", ["ゲッカンシ"], []),
        ("焼く", "やく", "to bake / grill / burn", ["ショウ"], ["や.く", "や.ける"]),
        ("焼肉", "やきにく", "grilled meat / yakiniku", [], ["やきにく"]),
    ],
    # Lesson 74[cite: 38]
    [
        ("焼ける", "やける", "to burn / be roasted / be sunburned", ["ショウ"], ["や.ける"]),
        ("すき焼き", "すきやき", "sukiyaki", [], ["すきやき"]),
        ("日焼け", "ひやけ", "sunburn / suntan", [], ["ひやけ"]),
        ("圧", "あつ", "pressure", ["アツ"], []),
        ("金魚", "きんぎょ", "goldfish", ["キンギョ"], []),
    ],
    # Lesson 75[cite: 38]
    [
        ("気圧", "きあつ", "atmospheric pressure", ["キアツ"], []),
        ("血圧", "けつあつ", "blood pressure", ["ケツアツ"], []),
        ("額", "がく", "framed picture / amount / forehead", ["ガク"], ["ひたい"]),
        ("半額", "はんがく", "half price", ["ハンガク"], []),
        ("断片", "だんぺん", "fragment / piece", ["ダンペン"], []),
    ],
    # Lesson 76[cite: 38]
    [
        ("金額", "きんがく", "amount of money", ["キンガク"], []),
        ("印", "しるし", "mark / sign / symbol / seal", ["イン"], ["しるし"]),
        ("目印", "めじるし", "landmark / guide / mark", [], ["めじるし"]),
        ("印象", "いんしょう", "impression", ["インショウ"], []),
        ("海辺", "うみべ", "seashore / beach", [], ["うみべ"]),
    ],
    # Lesson 77[cite: 38]
    [
        ("好印象", "こういんしょう", "good impression", ["コウインショウ"], []),
        ("印象的", "いんしょうてき", "impressive", ["インショウテキ"], []),
        ("池", "いけ", "pond", ["チ"], ["いけ"]),
        ("顔面", "がんめん", "face (anatomical)", ["ガンメン"], []),
        ("お家", "おうち", "home / house (polite)", [], ["おうち"]),
    ],
    # Lesson 78[cite: 38]
    [
        ("電池", "でんち", "battery", ["デンチ"], []),
        ("庫", "こ", "warehouse / storehouse", ["コ", "ク"], []),
        ("冷蔵庫", "れいぞうこ", "refrigerator", ["レイゾウコ"], []),
        ("農", "のう", "agriculture / farming", ["ノウ"], []),
        ("心構え", "こころがまえ", "preparedness / mental attitude", [], ["こころがまえ"]),
    ],
    # Lesson 79[cite: 38]
    [
        ("農業", "のうぎょう", "agriculture", ["ノウギョウ"], []),
        ("まな板", "まないた", "cutting board / chopping board", [], ["まないた"]),
        ("恋", "こい", "love / romance", ["レン"], ["こ.う", "こい", "こい.しい"]),
        ("恋しい", "こいしい", "beloved / missed / longed for", ["レン"], ["こい.しい"]),
        ("恋人", "こいびと", "lover / sweetheart", [], ["こいびと"]),
    ],
    # Lesson 80[cite: 38]
    [
        ("恋愛", "れんあい", "love / romantic love", ["レンアイ"], []),
        ("恋愛対象", "れんあいたいしょう", "romantic interest", ["レンアイタイショウ"], []),
        ("羽", "はね", "feather / wing / blade", ["ウ"], ["は", "はね"]),
        ("羽田", "はねだ", "Haneda", [], ["はねだ"]),
        ("羽根", "はね", "feather / shuttlecock", [], ["はね"]),
    ],
    # Lesson 81[cite: 38]
    [
        ("専ら", "もっぱら", "wholly / solely / exclusively", ["セン"], ["もっぱ.ら"]),
        ("専門", "せんもん", "specialty / major", ["センモン"], []),
        ("専門学校", "せんもんがっこう", "vocational / technical school", ["センモンガッコウ"], []),
        ("専業主婦", "せんぎょうしゅふ", "full-time housewife", ["センギョウシュフ"], []),
        ("発つ", "たつ", "to depart / leave", ["ハツ"], ["た.つ"]),
    ],
    # Lesson 82[cite: 38]
    [
        ("逆", "ぎゃく", "reverse / opposite", ["ギャク"], ["さか", "さか.らう"]),
        ("逆さ", "さかさ", "upside down / inverted", ["ギャク"], ["さか.さ"]),
        ("逆らう", "さからう", "to go against / oppose / disobey", ["ギャク"], ["さか.らう"]),
        ("逆様", "さかさま", "inverted / upside down", [], ["さかさま"]),
        ("反復", "はんぷく", "repetition", ["ハンプク"], []),
    ],
    # Lesson 83[cite: 38]
    [
        ("腕", "うで", "arm / skill / ability", ["ワン"], ["うで"]),
        ("短い", "みじかい", "short", ["タン"], ["みじか.い"]),
        ("短所", "たんしょ", "weak point / defect", ["タンショ"], []),
        ("短期", "たんき", "short-term", ["タンキ"], []),
        ("腕時計", "うでどけい", "wristwatch", [], ["うでどけい"]),
    ],
    # Lesson 84[cite: 38]
    [
        ("普", "ふ", "universal / wide", ["フ"], []),
        ("普通", "ふつう", "normal / ordinary / usual", ["フツウ"], []),
        ("普段", "ふだん", "usually / ordinarily", ["フダン"], []),
        ("岩", "いわ", "rock / crag", ["ガン"], ["いわ"]),
        ("短編", "たんぺん", "short story / short film", ["タンペン"], []),
    ],
    # Lesson 85[cite: 38]
    [
        ("児", "じ", "child / newborn", ["ジ", "ニ"], []),
        ("育児", "いくじ", "childcare / nursing", ["イクジ"], []),
        ("小児科", "しょうにか", "pediatrics", ["ショウニカ"], []),
        ("毛", "け", "hair / fur / wool", ["モウ"], ["け"]),
        ("丸太", "まるた", "log", [], ["まるた"]),
    ],
    # Lesson 86[cite: 38]
    [
        ("毛皮", "けがわ", "fur / pelt", [], ["けがわ"]),
        ("毛布", "もうふ", "blanket", ["モウフ"], []),
        ("毛糸", "けいと", "knitting wool / woolen yarn", [], ["けいと"]),
        ("髪の毛", "かみのけ", "hair (on head)", [], ["かみのけ"]),
        ("冊子", "さっし", "booklet / pamphlet", ["サッシ"], []),
    ],
    # Lesson 87[cite: 38]
    [
        ("版", "はん", "edition / printing / plate", ["ハン"], []),
        ("出版", "しゅっぱん", "publication", ["シュッパン"], []),
        ("出版社", "しゅっぱんしゃ", "publishing company", ["シュッパンシャ"], []),
        ("宇", "う", "eaves / universe / heaven", ["ウ"], []),
        ("近辺", "きんぺん", "neighborhood / vicinity", ["キンペン"], []),
    ],
    # Lesson 88[cite: 38]
    [
        ("況して", "まして", "still more / not to mention", ["キョウ"], ["ま.して"]),
        ("状況", "じょうきょう", "state of affairs / situation", ["ジョウキョウ"], []),
        ("被る", "かぶる", "to put on (one's head) / suffer", ["ヒ"], ["かぶ.る", "かぶ.せる"]),
        ("被せる", "かぶせる", "to cover (with something)", ["ヒ"], ["かぶ.せる"]),
        ("根性", "こんじょう", "willpower / guts / nature", ["コンジョウ"], []),
    ],
    # Lesson 89[cite: 38]
    [
        ("被害", "ひがい", "damage / harm / injury", ["ヒガイ"], []),
        ("被害者", "ひがいしゃ", "victim / injured party", ["ヒガイシャ"], []),
        ("岸", "きし", "bank / coast / shore", ["ガン"], ["きし"]),
        ("海岸", "かいがん", "coast / beach / seashore", ["カイガン"], []),
        ("破片", "はへん", "fragment / splinter / shard", ["ハヘン"], []),
    ],
    # Lesson 90[cite: 39]
    [
        ("超す", "こす", "to cross over / exceed / move", ["チョウ"], ["こ.える", "こ.す"]),
        ("超える", "こえる", "to exceed / surpass", ["チョウ"], ["こ.える"]),
        ("超過", "ちょうか", "excess / exceeding", ["チョウカ"], []),
        ("豊か", "ゆたか", "abundant / wealthy / rich", ["ホウ"], ["ゆた.か"]),
        ("代物", "しろもの", "article / goods / thing", [], ["しろもの"]),
    ],
    # Lesson 91[cite: 39]
    [
        ("豊富", "ほうふ", "abundant / plentiful", ["ホウフ"], []),
        ("含む", "ふくむ", "to contain / include", ["ガン"], ["ふく.む", "ふく.める"]),
        ("含める", "ふくめる", "to include / instruct", ["ガン"], ["ふく.める"]),
        ("植える", "うえる", "to plant / grow", ["ショク"], ["う.える", "う.わる"]),
        ("植物", "しょくぶつ", "plant / vegetation", ["ショクブツ"], []),
    ],
    # Lesson 92[cite: 39]
    [
        ("補う", "おぎなう", "to supplement / make up for", ["ホ"], ["おぎな.う"]),
        ("補習", "ほしゅう", "supplementary lessons", ["ホシュウ"], []),
        ("暴れる", "あばれる", "to act violently / rage", ["ボウ", "バク"], ["あば.れる", "あば.く"]),
        ("暴力", "ぼうりょく", "violence / force", ["ボウリョク"], []),
        ("渡辺", "わたなべ", "Watanabe (surname)", [], ["わたなべ"]),
    ],
    # Lesson 93[cite: 39]
    [
        ("課", "か", "lesson / section / department", ["カ"], []),
        ("日課", "にっか", "daily routine / daily lesson", ["ニッカ"], []),
        ("課長", "かちょう", "section manager", ["カチョウ"], []),
        ("跡", "あと", "trace / tracks / mark", ["セキ"], ["あと"]),
        ("腰痛", "ようつう", "lower back pain", ["ヨウツウ"], []),
    ],
    # Lesson 94[cite: 39]
    [
        ("足跡", "あしあと", "footprints", [], ["あしあと"]),
        ("虫", "むし", "insect / bug / worm", ["チュウ"], ["むし"]),
        ("虫歯", "むしば", "cavity / tooth decay", [], ["むしば"]),
        ("触る", "さわる", "to touch / feel", ["ショク"], ["さわ.る", "ふ.れる"]),
        ("触れる", "ふれる", "to touch / come in contact with", ["ショク"], ["ふ.れる"]),
    ],
    # Lesson 95[cite: 39]
    [
        ("お玉", "おたま", "ladle", [], ["おたま"]),
        ("水玉", "みずたま", "polka dots / water drop", [], ["みずたま"]),
        ("お年玉", "おとしだま", "New Year's gift money", [], ["おとしだま"]),
        ("震える", "ふるえる", "to shiver / shake / tremble", ["シン"], ["ふる.う", "ふる.える"]),
        ("彼岸", "ひがん", "equinoctial week / Nirvana", ["ヒガン"], []),
    ],
    # Lesson 96[cite: 39]
    [
        ("地震", "じしん", "earthquake", ["ジシン"], []),
        ("億", "おく", "hundred million", ["オク"], []),
        ("肩", "かた", "shoulder", ["ケン"], ["かた"]),
        ("肩こり", "かたこり", "stiff shoulders", [], ["かたこり"]),
        ("反る", "そる", "to warp / bend backward", ["ハン"], ["そ.る", "そ.らす"]),
    ],
    # Lesson 97[cite: 39]
    [
        ("肩書き", "かたがき", "title / degree / status", [], ["かたがき"]),
        ("劇", "げき", "drama / play", ["ゲキ"], []),
        ("悲劇", "ひげき", "tragedy", ["ヒゲキ"], []),
        ("劇場", "げきじょう", "theater / playhouse", ["ゲキジョウ"], []),
        ("借入金", "かりいれきん", "loan / borrowed money", [], ["かりいれきん"]),
    ],
    # Lesson 98[cite: 39]
    [
        ("演劇", "えんげき", "drama / theater", ["エンゲキ"], []),
        ("刺す", "さす", "to pierce / stab / sting", ["シ"], ["さ.す", "さ.さる"]),
        ("刺さる", "ささる", "to stick into / pierce", ["シ"], ["さ.さる"]),
        ("名刺", "めいし", "business card", ["メイシ"], []),
        ("並木", "なみき", "row of trees / avenue", [], ["なみき"]),
    ],
    # Lesson 99[cite: 39]
    [
        ("刺身", "さしみ", "sashimi (sliced raw fish)", [], ["さしみ"]),
        ("述べる", "のべる", "to state / express / mention", ["ジュツ"], ["の.べる"]),
        ("述語", "じゅつご", "predicate", ["ジュツゴ"], []),
        ("輪", "わ", "ring / wheel / circle", ["リン"], ["わ"]),
        ("五輪", "ごりん", "the Olympics", ["ゴリン"], []),
    ],
    # Lesson 100[cite: 39]
    [
        ("指輪", "ゆびわ", "finger ring", [], ["ゆびわ"]),
        ("浅い", "あさい", "shallow / superficial", ["セン"], ["あさ.い"]),
        ("浅草", "あさくさ", "Asakusa", [], ["あさくさ"]),
        ("純", "じゅん", "pure / genuine / innocent", ["ジュン"], []),
        ("金髪", "きんぱつ", "blond hair", ["キンパツ"], []),
    ],
    # Lesson 101[cite: 40]
    [
        ("単純", "たんじゅん", "simple / uncomplicated", ["タンジュン"], []),
        ("薄い", "うすい", "thin / pale / weak", ["ハク"], ["うす.い", "うす.める"]),
        ("薄暗い", "うすぐらい", "dim / gloomy", [], ["うすぐら.い"]),
        ("大阪", "おおさか", "Osaka", [], ["おおさか"]),
        ("固", "こ", "hard / solid / firm", ["コ"], ["かた.める", "かた.まる"]),
    ],
    # Lesson 102[cite: 40]
    [
        ("頑固", "がんこ", "stubborn / obstinate", ["ガンコ"], []),
        ("固まる", "かたまる", "to harden / solidify / gather", ["コ"], ["かた.まる"]),
        ("巨", "きょ", "gigantic / big / large", ["キョ"], []),
        ("巨大", "きょだい", "huge / gigantic / enormous", ["キョダイ"], []),
        ("韓", "かん", "Korea", ["カン"], []),
    ],
    # Lesson 103[cite: 40]
    [
        ("講ずる", "こうずる", "to lecture / take measures", ["コウ"], ["こう.ずる"]),
        ("聴講", "ちょうこう", "auditing (a lecture)", ["チョウコウ"], []),
        ("講演会", "こうえんかい", "lecture meeting", ["コウエンカイ"], []),
        ("舟", "ふね", "boat / small ship", ["シュウ"], ["ふね", "ふな-"]),
        ("詫書", "わびがき", "written apology", [], ["わびがき"]),
    ],
    # Lesson 104[cite: 40]
    [
        ("般", "はん", "sort / kind / general", ["ハン"], []),
        ("一般化", "いっぱんか", "generalization", ["イッパンカ"], []),
        ("一般的", "いっぱんてき", "general / common", ["イッパンテキ"], []),
        ("お湯", "おゆ", "hot water", ["トウ"], ["ゆ"]),
        ("一般", "いっぱん", "general / ordinary", ["イッパン"], []),
    ],
    # Lesson 105[cite: 40]
    [
        ("湯のみ", "ゆのみ", "teacup", [], ["ゆのみ"]),
        ("捨てる", "すてる", "to throw away / abandon", ["シャ"], ["す.てる"]),
        ("替える", "かえる", "to exchange / replace", ["タイ"], ["か.える", "か.わる"]),
        ("代替", "だいたい", "substitution / alternative", ["ダイタイ"], []),
        ("万歳", "ばんざい", "banzai / hooray", ["バンザイ"], []),
    ],
    # Lesson 106[cite: 40]
    [
        ("両替", "りょうがえ", "currency exchange", ["リョウガエ"], []),
        ("日替わり", "ひがわり", "daily special / changing daily", [], ["ひがわり"]),
        ("取り替える", "とりかえる", "to exchange / replace", [], ["とりか.える"]),
        ("央", "おう", "center / middle", ["オウ"], []),
        ("実る", "みのる", "to bear fruit / ripen", ["ジツ"], ["みの.る"]),
    ],
    # Lesson 107[cite: 40]
    [
        ("中央", "ちゅうおう", "center / central", ["チュウオウ"], []),
        ("骨", "ほね", "bone", ["コツ"], ["ほね"]),
        ("骨折", "こっせつ", "bone fracture", ["コッセツ"], []),
        ("齢", "れい", "age", ["レイ"], ["よわい"]),
        ("背骨", "せぼね", "backbone / spine", [], ["せぼね"]),
    ],
    # Lesson 108[cite: 40]
    [
        ("年齢", "ねんれい", "age / years", ["ネンレイ"], []),
        ("高齢", "こうれい", "advanced age / old age", ["コウレイ"], []),
        ("高齢者", "こうれいしゃ", "senior citizen / elderly person", ["コウレイシャ"], []),
        ("高齢化", "こうれいか", "aging of population", ["コウレイカ"], []),
        ("愛犬", "あいけん", "pet dog / beloved dog", ["アイケン"], []),
    ],
    # Lesson 109[cite: 40]
    [
        ("照る", "てる", "to shine", ["ショウ"], ["て.る", "て.らす"]),
        ("照らす", "てらす", "to illuminate / shine on", ["ショウ"], ["て.らす"]),
        ("対照", "たいしょう", "contrast / comparison", ["タイショウ"], []),
        ("層", "そう", "layer / stratum / class", ["ソウ"], []),
        ("一途", "いちず", "wholehearted / earnest", ["イチズ"], []),
    ],
    # Lesson 110[cite: 40]
    [
        ("高層ビル", "こうそうビル", "skyscraper / high-rise building", ["コウソウ"], []),
        ("弱い", "よわい", "weak / frail", ["ジャク"], ["よわ.い", "よわ.る"]),
        ("弱点", "じゃくてん", "weak point / weakness", ["ジャクテン"], []),
        ("築く", "きずく", "to build / construct", ["チク"], ["きず.く"]),
        ("植木", "うえき", "garden shrubs / potted plant", [], ["うえき"]),
    ],
    # Lesson 111[cite: 40]
    [
        ("建築", "けんちく", "construction / architecture", ["ケンチク"], []),
        ("脳", "のう", "brain", ["ノウ"], []),
        ("頭脳", "ずのう", "brains / intellect", ["ズノウ"], []),
        ("航する", "こうする", "to sail / navigate", ["コウ"], []),
        ("脳裏", "のうり", "one's mind / back of one's mind", ["ノウリ"], []),
    ],
    # Lesson 112[cite: 40]
    [
        ("航空便", "こうくうびん", "airmail", ["コウクウビン"], []),
        ("快い", "こころよい", "pleasant / agreeable", ["カイ"], ["こころよ.い"]),
        ("快適", "かいてき", "pleasant / comfortable", ["カイテキ"], []),
        ("快晴", "かいせい", "clear weather / cloudless sky", ["カイセイ"], []),
        ("機内", "きない", "in-flight / inside the plane", ["キナイ"], []),
    ],
    # Lesson 113[cite: 40]
    [
        ("翌日", "よくじつ", "the next day", ["ヨクジツ"], []),
        ("翌年", "よくねん", "the following year", ["ヨクネン"], []),
        ("翌月", "よくげつ", "the following month", ["ヨクゲツ"], []),
        ("翌週", "よくしゅう", "the following week", ["ヨクシュウ"], []),
        ("翌", "よく", "following / next", ["ヨク"], []),
    ],
    # Lesson 114[cite: 40]
    [
        ("旧", "きゅう", "old / former", ["キュウ"], ["ふる.い"]),
        ("筆", "ふで", "writing brush", ["ヒツ"], ["ふで"]),
        ("筆者", "ひっしゃ", "writer / author", ["ヒッシャ"], []),
        ("仲える", "つかえる", "to serve / work under", ["チュウ"], ["つか.える"]),
        ("湯気", "ゆげ", "steam / vapor", [], ["ゆげ"]),
    ],
    # Lesson 115[cite: 40]
    [
        ("交換", "こうかん", "exchange / replacement", ["コウカン"], []),
        ("変換", "へんかん", "conversion / transformation", ["ヘンカン"], []),
        ("乗り換える", "のりかえる", "to transfer (trains/buses)", [], ["のりか.える"]),
        ("群れ", "むれ", "group / crowd / flock / herd", ["グン"], ["む.れる", "む.れ"]),
        ("抜群", "ばつぐん", "outstanding / preeminent", ["バツグン"], []),
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

    for l_idx, chunk in enumerate(N2_PART1_DATA):
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
                "id": f"n2-{item_counter}",
                "level": "N2",
                "word": word,
                "kana": kana,
                "meaning": meaning,
                "onyomi": onyomi,
                "kunyomi": kunyomi,
                "characters": characters_data,
            })
            item_counter += 1

        lessons.append({
            "id": f"n2-lesson-{lesson_num}",
            "level": "N2",
            "lessonNumber": lesson_num,
            "items": lesson_items,
        })

    with open(PART1_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(lessons, f, ensure_ascii=False)

    print(f"Part 1 complete! Saved Lessons 1-115 ({item_counter - 1} items) to {PART1_JSON_PATH}.")


if __name__ == "__main__":
    main()