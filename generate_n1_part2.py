import os
import json
import xml.etree.ElementTree as ET

KANJIVG_DIR = "kanjivg-data"
PART1_JSON_PATH = "n1_part1.json"
PART2_JSON_PATH = "n1_part2.json"

N1_PART2_DATA = [
    # Lesson 126[cite: 38]
    [
        ("信仰", "しんこう", "religious faith / belief / creed", ["シンコウ"], []),
        ("瀬", "せ", "rapids / current / torrent / shallows / shoal", ["ライ"], ["せ"]),
        ("瀬戸物", "せともの", "earthenware / crockery / china / porcelain", ["セトモノ"], []),
        ("致す", "いたす", "to do (humble)", ["チ"], ["いた.す"]),
        ("就職", "しゅうしょく", "finding employment / getting a job", ["シュウショク"], []),
    ],
    # Lesson 127[cite: 38]
    [
        ("合致", "がっち", "agreement / concurrence / conformity / coincidence", ["ガッチ"], []),
        ("一致", "いっち", "coincidence / agreement / union / match", ["イッチ"], []),
        ("伏す", "ふす", "to bend down / bow down / prostrate oneself", ["フク"], ["ふ.す", "ふ.せる"]),
        ("降伏", "こうふく", "capitulation / surrender / submission", ["コウフク"], []),
        ("締結", "ていけつ", "conclusion (of a treaty, contract, etc.)", ["テイケツ"], []),
    ],
    # Lesson 128[cite: 38]
    [
        ("起伏", "きふく", "undulation / ups and downs / highs and lows", ["キフク"], []),
        ("杉", "すぎ", "Japanese cedar (Cryptomeria japonica)", ["サン"], ["すぎ"]),
        ("避ける", "さける", "to avoid (physical contact with) / ward off / avert", ["ヒ"], ["さ.ける", "よ.ける"]),
        ("揺れる", "ゆれる", "to shake / sway / waver / tremble", ["ヨウ"], ["ゆ.れる", "ゆ.る"]),
        ("消滅", "しょうめつ", "extinction / extinguishment / disappearance", ["ショウメツ"], []),
    ],
    # Lesson 129[cite: 38]
    [
        ("執る", "とる", "to take (trouble) / attend (to business) / command", ["シツ", "シュウ"], ["と.る"]),
        ("執筆", "しっぴつ", "writing (e.g. as a profession)", ["シッピツ"], []),
        ("崩す", "くずす", "to destroy / demolish / pull down / tear down", ["ホウ"], ["くず.す", "くず.れる"]),
        ("崩れる", "くずれる", "to collapse / crumble / fall into ruin", ["ホウ"], ["くず.れる"]),
        ("崩壊", "ほうかい", "collapse / crumbling / breaking down / caving in", ["ホウカイ"], []),
    ],
    # Lesson 130[cite: 38]
    [
        ("酸っぱい", "すっぱい", "sour / acid", ["サン"], ["す.っぱい"]),
        ("銃", "じゅう", "gun / rifle / small arms", ["ジュウ"], ["つつ"]),
        ("縄", "なわ", "rope / cord", ["ジョウ"], ["なわ", "ただ.す"]),
        ("詩", "し", "poem / poetry", ["シ"], ["うた"]),
        ("目覚める", "めざめる", "to wake up / awake / come to one's senses", [], ["めざ.める"]),
    ],
    # Lesson 131[cite: 38]
    [
        ("詩人", "しじん", "poet", ["シジン"], []),
        ("廃れる", "すたれる", "to go out of use / become obsolete / die out", ["ハイ"], ["すた.れる", "すた.る"]),
        ("荒廃", "こうはい", "ruin / destruction / devastation / decay", ["コウハイ"], []),
        ("廃止", "はいし", "abolition / repeal", ["ハイシ"], []),
        ("素人", "しろうと", "layman / amateur / novice", ["ソジン"], ["しろうと"]),
    ],
    # Lesson 132[cite: 38]
    [
        ("充てる", "あてる", "to assign / allot / allocate / apply", ["ジュウ"], ["あ.てる", "み.たす"]),
        ("充電", "じゅうでん", "charging (electrically) / electrification", ["ジュウデン"], []),
        ("鏡", "かがみ", "mirror / looking-glass", ["キョウ", "ケイ"], ["かがみ"]),
        ("眼鏡", "めがね", "glasses / eyeglasses / spectacles", ["ガンキョウ"], ["めがね"]),
        ("振込", "ふりこみ", "payment made via bank deposit transfer", [], ["ふりこみ"]),
    ],
    # Lesson 133[cite: 38]
    [
        ("仮に", "かりに", "temporarily / provisionally / for argument's sake", ["カ", "ケ"], ["かり.に"]),
        ("仮令", "たとい", "even if / although", ["カレイ"], ["たと.い"]),
        ("仮名", "かな", "kana / Japanese syllabary", ["カナ", "ケミョウ"], []),
        ("仮定", "かてい", "assumption / supposition / hypothesis", ["カテイ"], []),
        ("歩む", "あゆむ", "to walk / go on foot", ["ホ", "ブ", "フ"], ["あゆ.む", "ある.く"]),
    ],
    # Lesson 134[cite: 38]
    [
        ("片仮名", "かたかな", "katakana", ["カタカナ"], []),
        ("平仮名", "ひらがな", "hiragana", ["ヒラガナ"], []),
        ("振り仮名", "ふりがな", "furigana / ruby characters", [], ["ふりがな"]),
        ("仮名遣い", "かなづかい", "kana orthography / syllabary spelling", [], ["かなづかい"]),
        ("疲労", "ひろう", "fatigue / weariness", ["ヒロウ"], []),
    ],
    # Lesson 135[cite: 38]
    [
        ("送り仮名", "おくりがな", "okurigana / kana suffixes following kanji stems", [], ["おくりがな"]),
        ("吐く", "はく", "to vomit / throw up / spit up / emit / breathe", ["ト"], ["は.く", "つ.く"]),
        ("吐き気", "はきけ", "nausea / sickness in the stomach", [], ["はきけ"]),
        ("請", "せい", "solicit / invite / ask", ["セイ", "シン", "ショウ"], ["こ.う", "う.ける"]),
        ("申請", "しんせい", "application / request / petition", ["シンセイ"], []),
    ],
    # Lesson 136[cite: 38]
    [
        ("請求書", "せいきゅうしょ", "invoice / bill / written claim", ["セイキュウショ"], []),
        ("眺め", "ながめ", "scene / view / prospect / outlook", ["チョウ"], ["なが.め"]),
        ("眺める", "ながめる", "to look at / gaze at / watch / stare at", ["チョウ"], ["なが.める"]),
        ("沖", "おき", "open sea", ["チュウ"], ["おき"]),
        ("街道", "かいどう", "highway (esp. one existing from the Edo period)", ["カイドウ"], []),
    ],
    # Lesson 137[cite: 38]
    [
        ("沖縄", "おきなわ", "Okinawa", [], ["おきなわ"]),
        ("躍り", "おどり", "jump / leap / spring / dance", ["ヤク"], ["おど.り"]),
        ("活躍", "かつやく", "activity (esp. energetic) / great efforts", ["カツヤク"], []),
        ("威", "い", "intimidate / dignity / majesty / menace / threaten", ["イ"], ["おど.す", "おど.し"]),
        ("無言", "むごん", "silence (not speaking) / muteness", ["ムゴン"], []),
    ],
    # Lesson 138[cite: 39]
    [
        ("権威", "けんい", "authority / power / influence", ["ケンイ"], []),
        ("威力", "いりょく", "power / might / authority / influence", ["イリョク"], []),
        ("威張る", "いばる", "to put on airs / act big / throw one's weight about", ["イ"], ["いば.る"]),
        ("屈する", "くっする", "to yield to / give in to / submit to / bend", ["クツ"], ["くっ.する"]),
        ("浮気", "うわき", "extramarital sex / affair / infidelity / fickleness", ["ウワキ"], []),
    ],
    # Lesson 139[cite: 39]
    [
        ("屈折", "くっせつ", "bending / indentation / refraction (of light)", ["クッセツ"], []),
        ("退屈", "たいくつ", "tedium / boredom / dullness", ["タイクツ"], []),
        ("理屈", "りくつ", "theory / reason / logic / pretext / argument", ["リクツ"], []),
        ("勘", "かん", "perception / intuition / the sixth sense", ["カン"], []),
        ("富む", "とむ", "to be rich in / abound in / be abundant in", ["フ", "フウ"], ["と.む", "とみ"]),
    ],
    # Lesson 140[cite: 39]
    [
        ("勘定", "かんじょう", "calculation / counting / consideration / bill", ["カンジョウ"], []),
        ("割り勘", "わりかん", "splitting the bill / going Dutch", [], ["わりかん"]),
        ("徹する", "てっする", "to sink in / penetrate / devote oneself to", ["テツ"], ["てっ.する"]),
        ("徹底", "てってい", "thoroughness / completeness", ["テッテイ"], []),
        ("類似", "るいじ", "resemblance / similarity / likeness / analogy", ["ルイジ"], []),
    ],
    # Lesson 141[cite: 39]
    [
        ("徹夜", "てつや", "staying up all night", ["テツヤ"], []),
        ("斉", "せい", "adjusted / alike / equal / similar variety of", ["セイ", "サイ"], ["そろ.う", "ひと.しい"]),
        ("斎", "さい", "purification / Buddhist food / room / worship", ["サイ"], ["とき", "つつし.む"]),
        ("謝る", "あやまる", "to apologize / beg pardon", ["シャ"], ["あやま.る"]),
        ("柔軟", "じゅうなん", "flexible / lithe / soft / pliable", ["ジュウナン"], []),
    ],
    # Lesson 142[cite: 39]
    [
        ("感謝", "かんしゃ", "thanks / gratitude", ["カンシャ"], []),
        ("艦", "かん", "warship", ["カン"], []),
        ("軍艦", "ぐんかん", "warship / battleship", ["グンカン"], []),
        ("催す", "もよおす", "to hold (an event) / give (a dinner) / feel", ["サイ"], ["もよお.す"]),
        ("度々", "たびたび", "often / again and again / frequently / repeatedly", ["ド", "ト"], ["たびたび"]),
    ],
    # Lesson 143[cite: 39]
    [
        ("催し", "もよおし", "event / festivities / function / social gathering", ["サイ"], ["もよお.し"]),
        ("主催", "しゅさい", "sponsorship (i.e. conducting under one's auspices)", ["シュサイ"], []),
        ("開催", "かいさい", "holding (a conference, exhibition, etc.) / opening", ["カイサイ"], []),
        ("舎", "しゃ", "cottage / inn / hut / house / mansion", ["シャ", "セキ"], ["やど.る"]),
        ("遺言", "ゆいごん", "will / testament / last request", ["ユイゴン", "イゴン"], []),
    ],
    # Lesson 144[cite: 39]
    [
        ("田舎", "いなか", "rural area / countryside / the sticks / hometown", ["デンシャ"], ["いなか"]),
        ("衝", "しょう", "collide / brunt / highway / opposition (astronomy)", ["ショウ"], ["つ.く"]),
        ("脚", "あし", "foot / leg / gait / pace / undercarriage", ["キャク", "キャ", "カク"], ["あし"]),
        ("脚色", "きゃくしょく", "dramatization (e.g. of a novel) / adaptation", ["キャクショク"], []),
        ("眼差し", "まなざし", "look / gaze / glance", [], ["まなざし"]),
    ],
    # Lesson 145[cite: 39]
    [
        ("虎", "とら", "tiger / drunkard", ["コ"], ["とら"]),
        ("潮", "しお", "tide / current / salt water / opportunity", ["チョウ"], ["しお", "うしお"]),
        ("穴", "あな", "hole / opening / orifice / perforation", ["ケツ"], ["あな"]),
        ("怪しい", "あやしい", "suspicious / dubious / doubtful / dodgy", ["カイ", "ケ"], ["あや.しい", "あや.しむ"]),
        ("怪我", "けが", "injury (to animate object) / hurt", ["ケガ"], []),
    ],
    # Lesson 146[cite: 39]
    [
        ("仙", "せん", "hermit / wizard / cent", ["セン", "セント"], []),
        ("仙台", "せんだい", "Sendai", ["センダイ"], []),
        ("輝く", "かがやく", "to shine / glitter / sparkle", ["キ"], ["かがや.く"]),
        ("緊", "きん", "tense / solid / hard / reliable / tight", ["キン"], ["し.める", "し.まる"]),
        ("騒音", "そうおん", "noise", ["ソウオン"], []),
    ],
    # Lesson 147[cite: 39]
    [
        ("緊張", "きんちょう", "tension / mental strain / nervousness", ["キンチョウ"], []),
        ("唇", "くちびる", "lips", ["シン"], ["くちびる"]),
        ("狂う", "くるう", "to go mad / lose one's mind / go crazy / get out of order", ["キョウ"], ["くる.う", "くる.おしい"]),
        ("厳密", "げんみつ", "strict / close / precise / accurate", ["ゲンミツ"], []),
        ("寿司", "すし", "sushi", ["スシ"], []),
    ],
    # Lesson 148[cite: 39]
    [
        ("奪う", "うばう", "to snatch away / dispossess / steal / rob", ["ダツ"], ["うば.う"]),
        ("診る", "みる", "to examine (medically)", ["シン"], ["み.る"]),
        ("診察", "しんさつ", "medical examination", ["シンサツ"], []),
        ("診察券", "しんさつけん", "patient's registration card (at a hospital/clinic)", ["シンサツケン"], []),
        ("入浴", "にゅうよく", "bathing / taking a bath", ["ニュウヨク"], []),
    ],
    # Lesson 149[cite: 39]
    [
        ("診察室", "しんさつしつ", "consultation room / examination room", ["シンサツシツ"], []),
        ("診察時間", "しんさつじかん", "consultation hours / doctor's office hours", ["シンサツジカン"], []),
        ("健康診断", "けんこうしんだん", "health examination / medical checkup", ["ケンコウシンダン"], []),
        ("債", "さい", "bond / loan / debt", ["サイ"], []),
        ("取締役", "とりしまりやく", "company director / board member", [], ["とりしまりやく"]),
    ],
    # Lesson 150[cite: 39]
    [
        ("負債", "ふさい", "debt / liabilities", ["フサイ"], []),
        ("鈴", "すず", "bell", ["レイ", "リン"], ["すず"]),
        ("僧", "そう", "Buddhist priest / monk", ["ソウ"], []),
        ("掲げる", "かかげる", "to put up (a notice, sign, etc.) / hold up / hoist", ["ケイ"], ["かか.げる"]),
        ("大豆", "だいず", "soybean / soya bean", ["ダイズ"], []),
    ],
    # Lesson 151[cite: 40]
    [
        ("掲示板", "けいじばん", "bulletin board / display board / notice board", ["ケイジバン"], []),
        ("伯", "はく", "chief / count / earl / uncle / Brazil", ["ハク"], []),
        ("伯父さん", "おじさん", "uncle (older than one's parent)", ["ハクフ"], ["おじさん"]),
        ("梅", "うめ", "Japanese apricot (Prunus mume) / plum", ["バイ"], ["うめ"]),
        ("伯父", "おじ", "uncle (older than one's parent)", ["ハクフ"], ["おじ"]),
    ],
    # Lesson 152[cite: 40]
    [
        ("梅雨", "つゆ", "rainy season (in Japan, usually early June to mid-July)", ["バイウ"], ["つゆ"]),
        ("梅雨", "ばいう", "rainy season", ["バイウ"], ["つゆ"]),
        ("看", "かん", "watch over / see", ["カン"], ["み.る"]),
        ("看護師", "かんごし", "nurse (hospital)", ["カンゴシ"], []),
        ("発掘", "はっくつ", "excavation / exhumation / unearthing", ["ハックツ"], []),
    ],
    # Lesson 153[cite: 40]
    [
        ("摘む", "つむ", "to pick / pluck / trim", ["テキ"], ["つ.む"]),
        ("指摘", "してき", "pointing out / identification", ["シテキ"], []),
        ("項", "こう", "paragraph / clause / item / nape of neck", ["コウ"], ["うなじ"]),
        ("項目", "こうもく", "item / heading / category / clause", ["コウモク"], []),
        ("戸籍", "こせき", "family register / census register", ["コセキ"], []),
    ],
    # Lesson 154[cite: 40]
    [
        ("霊", "れい", "spirits / soul", ["レイ", "リョウ"], ["たま"]),
        ("垣", "かき", "hedge / fence / wall", ["エン"], ["かき"]),
        ("垣根", "かきね", "hedge / fence", [], ["かきね"]),
        ("慢ずる", "まんずる", "to be proud / boast / neglect", ["マン"], ["まん.ずる"]),
        ("井戸", "いど", "water well", [], ["いど"]),
    ],
    # Lesson 155[cite: 40]
    [
        ("我慢", "がまん", "patience / endurance / perseverance / tolerance", ["ガマン"], []),
        ("自慢", "じまん", "pride / boast", ["ジマン"], []),
        ("扱う", "あつかう", "to deal with (a person) / treat / handle / take care of", ["キュウ", "ソウ"], ["あつか.う"]),
        ("如", "じょ", "likeness / like / such as / as if / better / best", ["ジョ", "ニョ"], ["ごと.し"]),
        ("如何", "いかが", "how / in what way / how about", ["イカ"], ["いかが"]),
    ],
    # Lesson 156[cite: 40]
    [
        ("縮む", "ちぢむ", "to shrink / contract / diminish (in size)", ["シュク"], ["ちぢ.む", "ちぢ.まる"]),
        ("詳しい", "くわしい", "detailed / full / accurate / well-informed", ["ショウ"], ["くわ.しい"]),
        ("旦つく", "たんつく", "to dawn / become day", ["タン"], []),
        ("元旦", "がんたん", "New Year's Day (esp. morning of January 1)", ["ガンタン"], []),
        ("詳細", "しょうさい", "details / particulars", ["ショウサイ"], []),
    ],
    # Lesson 157[cite: 40]
    [
        ("慮", "りょ", "prudence / thought / concern / consider / deliberate", ["リョ"], ["おもんぱく.る", "おもんぱか.る"]),
        ("遠慮", "えんりょ", "restraint / reserve / hesitation / holding back", ["エンリョ"], []),
        ("雅", "みやび", "refinement / grace / elegance", ["ガ"], ["みや.び"]),
        ("雅致", "がち", "good taste / elegance / grace", ["ガチ"], []),
        ("取扱", "とりあつかい", "treatment / service / handling / management", [], ["とりあつかい"]),
    ],
    # Lesson 158[cite: 40]
    [
        ("砲", "ほう", "cannon / gun", ["ホウ"], []),
        ("鉄砲", "てっぽう", "gun / firearm", ["テッポウ"], []),
        ("懐かしい", "なつかしい", "dear / desired / missed / nostalgic", ["カイ"], ["なつか.しい", "なつか.しむ"]),
        ("人懐っこい", "ひとなつっこい", "friendly / affable / amiable", [], ["ひとなつっこ.い"]),
        ("如何なる", "いかなる", "what kind of / any / whatsoever", [], ["いかなる"]),
    ],
    # Lesson 159[cite: 40]
    [
        ("愚か", "おろか", "foolish / stupid", ["グ"], ["おろ.か"]),
        ("駄", "だ", "burdensome / pack horse / horse load / trivial", ["ダ", "タ"], []),
        ("無駄", "むだ", "futility / waste / uselessness / pointlessness", ["ムダ"], []),
        ("仕える", "つかえる", "to serve / work for / attend", ["シ", "ジ"], ["つか.える"]),
    ],
    # Lesson 160[cite: 40]
    [
        ("無駄遣い", "むだづかい", "waste (of money, time, etc.) / squandering", [], ["むだづかい"]),
        ("奴", "やつ", "fellow / guy / chap / thing / object", ["ド"], ["やつ", "やっこ"]),
        ("銭", "ぜに", "coin / money", ["セン", "ゼン"], ["ぜに"]),
        ("小銭", "こぜに", "coins / small change", [], ["こぜに"]),
        ("奴ら", "やつら", "they / those guys", ["ド"], ["やつら"]),
    ],
    # Lesson 161[cite: 40]
    [
        ("抑え", "おさえ", "weight / rear guard / control / check / restraint", ["ヨク"], ["おさ.え"]),
        ("侍", "さむらい", "warrior / samurai", ["ジ", "シ"], ["さむらい", "はべ.る"]),
        ("宙", "ちゅう", "mid-air / air / space / sky / memorization", ["チュウ"], []),
        ("宇宙", "うちゅう", "universe / cosmos / space", ["ウチュウ"], []),
        ("抑制", "よくせい", "control / restraint / suppression / constraint", ["ヨクセイ"], []),
    ],
    # Lesson 162[cite: 40]
    [
        ("範", "はん", "pattern / example / model", ["ハン"], []),
        ("模範", "もはん", "exemplar / model / pattern / example", ["モハン"], []),
        ("範囲", "はんい", "extent / scope / sphere / range / span", ["ハンイ"], []),
        ("規範", "きはん", "model / standard / pattern / norm / criterion", ["キハン"], []),
        ("仕舞", "しまい", "end / closing / being done for", [], ["しまい"]),
    ],
    # Lesson 163[cite: 40]
    [
        ("潜る", "くぐる", "to go under / pass under / go through / dive", ["セン"], ["くぐ.る", "もぐ.る"]),
        ("潜る", "もぐる", "to dive (into or under water) / go underground", ["セン"], ["もぐ.る", "くぐ.る"]),
        ("潜入", "せんにゅう", "infiltration / sneaking in", ["センニュウ"], []),
        ("潜水", "せんすい", "diving / submerging", ["センスイ"], []),
        ("潜む", "ひそむ", "to lurk / be hidden / be concealed / lie dormant", ["セン"], ["ひそ.む"]),
    ],
    # Lesson 164[cite: 41]
    [
        ("酔う", "よう", "to get drunk / become intoxicated / feel sick (motion)", ["スイ"], ["よ.う"]),
        ("酔っ払い", "よっぱらい", "drunkard / boozer", [], ["よっぱらい"]),
        ("酔っ払う", "よっぱらう", "to get drunk", [], ["よっぱら.う"]),
        ("呂", "ろ", "spine / backbone", ["ロ", "リョ"], ["せぼね"]),
        ("風呂", "ふろ", "bath / bathtub / bathroom / bathhouse", ["フロ"], []),
    ],
    # Lesson 165[cite: 41]
    [
        ("お風呂", "おふろ", "bath / bathtub", ["フロ"], []),
        ("亜", "あ", "Asia / rank next / come after / -ous", ["ア"], ["つ.ぐ"]),
        ("亜科", "あか", "subfamily (biology)", ["アカ"], []),
        ("沼", "ぬま", "marsh / lake / bog / pond / swamp", ["ショウ"], ["ぬま"]),
        ("負傷", "ふしょう", "injury / wound", ["フショウ"], []),
    ],
    # Lesson 166[cite: 41]
    [
        ("巡る", "めぐる", "to go around / make a circuit of / surround", ["ジュン"], ["めぐ.る", "めぐ.り"]),
        ("お巡りさん", "おまわりさん", "police officer (friendly term)", [], ["おまわりさん"]),
        ("巡査", "じゅんさ", "police officer / constable", ["ジュンサ"], []),
        ("臭い", "くさい", "stinking / smelly / suspicious / fishy", ["シュウ"], ["くさ.い", "にお.う"]),
        ("黄金", "おうごん", "gold / money", ["オウゴン"], ["こがね"]),
    ],
    # Lesson 167[cite: 41]
    [
        ("臭う", "におう", "to smell / stink / give off a smell", ["シュウ"], ["にお.う"]),
        ("慶", "けい", "jubilation / congratulate / rejoice / be happy", ["ケイ"], ["よろこ.び"]),
        ("慶ぶ", "よろこぶ", "to be delighted / be glad / rejoice", ["ケイ"], ["よろこ.ぶ"]),
        ("距", "きょ", "long-distance / spur / fetlock", ["キョ"], ["へだ.たる"]),
        ("脱出", "だっしゅつ", "escape / breakout / extrication", ["ダッシュツ"], []),
    ],
    # Lesson 168[cite: 41]
    [
        ("距離", "きょり", "distance / range", ["キョリ"], []),
        ("侵す", "おかす", "to invade / raid / trespass / violate / intrude on", ["シン"], ["おか.す"]),
        ("侵略", "しんりゃく", "aggression / invasion / raid", ["シンリャク"], []),
        ("侵入", "しんにゅう", "invasion / incursion / raid / aggression / intrusion", ["シンニュウ"], []),
        ("挙句", "あげく", "in the end (after a long process) / finally", ["アゲク"], []),
    ],
    # Lesson 169[cite: 41]
    [
        ("同僚", "どうりょう", "coworker / colleague / associate", ["ドウリョウ"], []),
        ("悟る", "さとる", "to perceive / sense / discern / understand / attain enlightenment", ["ゴ"], ["さと.る"]),
        ("覚悟", "かくご", "resolution / resignation / readiness / preparedness", ["カクゴ"], []),
        ("裂く", "さく", "to tear / rip / split / rend / sever", ["レツ"], ["さ.く", "さ.ける"]),
        ("僚", "りょう", "colleague / official / companion", ["リョウ"], []),
    ],
    # Lesson 170[cite: 41]
    [
        ("裂ける", "さける", "to split / tear / burst / be torn", ["レツ"], ["さ.ける"]),
        ("破裂", "はれつ", "explosion / rupture / break off", ["ハレツ"], []),
        ("分裂", "ぶんれつ", "split / division / break up / fission", ["ブンレツ"], []),
        ("尋ねる", "たずねる", "to ask / enquire / inquire / search / look for", ["ジン"], ["たず.ねる"]),
        ("強いる", "しいる", "to force / compel / coerce / press", ["キョウ", "ゴウ"], ["し.いる"]),
    ],
    # Lesson 171[cite: 41]
    [
        ("旗", "はた", "flag", ["キ"], ["はた"]),
        ("票", "ひょう", "ballot / label / ticket / sign", ["ヒョウ"], []),
        ("投票", "とうひょう", "voting / poll", ["トウヒョウ"], []),
        ("稲", "いね", "rice plant", ["トウ", "テ"], ["いね", "いな-"]),
        ("半端", "はんぱ", "remnant / fragment / incomplete / half-hearted", ["ハンパ"], []),
    ],
    # Lesson 172[cite: 41]
    [
        ("稲光", "いなびかり", "flash of lightning", [], ["いなびかり"]),
        ("一生懸命", "いっしょうけんめい", "very hard / with utmost effort / for dear life", ["イッショウケンメイ"], []),
        ("稿", "こう", "draft / copy / manuscript / straw", ["コウ"], ["わら", "したがき"]),
        ("原稿", "げんこう", "manuscript / copy", ["ゲンコウ"], []),
        ("懸", "けん", "state of suspension / hang / depend", ["ケン", "ケ"], ["か.ける", "か.かる"]),
    ],
    # Lesson 173[cite: 41]
    [
        ("盤", "ばん", "tray / shallow bowl / platter / tub / board / phonograph record", ["バン"], []),
        ("算盤", "そろばん", "abacus", ["サンバン"], ["そろばん"]),
        ("基盤", "きばん", "foundation / basis / base / infrastructure", ["キバン"], []),
        ("地盤", "じばん", "ground / crust (earth) / foundation / base / constituency", ["ジバン"], []),
        ("懸念", "けねん", "worry / fear / anxiety / concern", ["ケネン"], []),
    ],
    # Lesson 174[cite: 41]
    [
        ("災い", "わざわい", "calamity / disaster / misfortune", ["サイ"], ["わざわ.い"]),
        ("戦災", "せんさい", "war damage", ["センサイ"], []),
        ("災害", "さいがい", "calamity / disaster / misfortune", ["サイガイ"], []),
        ("災難", "さいなん", "calamity / misfortune / disaster", ["サイナン"], []),
        ("麻薬", "まやく", "narcotic / drug / dope", ["マヤク"], []),
    ],
    # Lesson 175[cite: 41]
    [
        ("天災", "てんさい", "natural calamity / natural disaster", ["テンサイ"], []),
        ("火災", "かさい", "conflagration / fire", ["カサイ"], []),
        ("尽くす", "つくす", "to use up / exhaust / run out of / devote oneself to", ["ジン", "サン"], ["つ.くす", "つ.きる"]),
        ("尽きる", "つきる", "to be used up / be run out / be exhausted / come to an end", ["ジン"], ["つ.きる"]),
        ("乳房", "ちぶさ", "breast / udder", ["ニュウボウ"], ["ちぶさ"]),
    ],
    # Lesson 176[cite: 41]
    [
        ("繁", "はん", "luxuriant / thick / overgrown / frequency / complexity / trouble", ["ハン"], ["しげ.る"]),
        ("繁栄", "はんえい", "prospering / prosperity / thriving / flourishing", ["ハンエイ"], []),
        ("繁盛", "はんじょう", "prosperity / flourishing / thriving", ["ハンジョウ"], []),
        ("即ち", "すなわち", "that is / namely / i.e.", ["ソク"], ["すなわ.ち"]),
        ("恥", "はじ", "shame / embarrassment / disgrace", ["チ"], ["はじ", "は.じる"]),
    ],
    # Lesson 177[cite: 42]
    [
        ("即する", "そくする", "to conform to / agree with / be adapted to / be based on", ["ソク"], ["そく.する"]),
        ("即座に", "そくざに", "immediately / right away / on the spot", ["ソクザ"], []),
        ("帳", "ちょう", "notebook / account book / album / curtain / veil", ["チョウ"], ["とばり"]),
        ("手帳", "てちょう", "pocket notebook / memo pad / planner", ["テチョウ"], []),
        ("振替", "ふりかえ", "change / switch / transfer (money)", [], ["ふりかえ"]),
    ],
    # Lesson 178[cite: 42]
    [
        ("貯金通帳", "ちょきんつうちょう", "savings passbook / bankbook", ["チョキンツウチョウ"], []),
        ("預金通帳", "よきんつうちょう", "bankbook / passbook", ["ヨキンツウチョウ"], []),
        ("飾る", "かざる", "to decorate / ornament / adorn", ["ショク"], ["かざ.る"]),
        ("沿い", "ぞい", "along", ["エン"], ["ぞ.い"]),
        ("末期", "まっき", "closing years (period, days) / last stage / terminal", ["マッキ", "マツゴ"], []),
    ],
    # Lesson 179[cite: 42]
    [
        ("沿う", "そう", "to run along / follow / conform to / meet (expectations)", ["エン"], ["そ.う"]),
        ("沿岸", "えんがん", "coast / shore", ["エンガン"], []),
        ("沿線", "えんせん", "along a railway line", ["エンセン"], []),
        ("獲", "かく", "seize / get / find / earn / acquire / can / may / able to", ["カク"], ["え.る"]),
        ("損なう", "そこなう", "to harm / hurt / injure / damage / fail in doing", ["ソン"], ["そこ.なう", "そこ.ねる"]),
    ],
    # Lesson 180[cite: 42]
    [
        ("獲物", "えもの", "game / spoils / trophy / catch / prey", ["カクブツ"], ["えもの"]),
        ("捕獲", "ほかく", "capture / seizure", ["ホカク"], []),
        ("獲得", "かくとく", "acquisition / possession", ["カクトク"], []),
        ("伴う", "ともなう", "to accompany / go hand in hand with / entail", ["ハン", "バン"], ["ともな.う"]),
        ("装飾", "そうしょく", "ornament / decoration", ["ソウショク"], []),
    ],
    # Lesson 181[cite: 42]
    [
        ("狭い", "せまい", "narrow / confined / small", ["キョウ", "コウ"], ["せま.い", "せば.める"]),
        ("添う", "そう", "to accompany / become married to / comply with", ["テン"], ["そ.う", "そ.える"]),
        ("添える", "そえる", "to garnish / accompany (as a card does a gift) / add to", ["テン"], ["そ.える"]),
        ("添付", "てんぷ", "attachment / affixing / appending", ["テンプ"], []),
        ("値する", "あたいする", "to be worth / be worthy of / deserve / merit", ["チ"], ["あたい.する"]),
    ],
    # Lesson 182[cite: 42]
    [
        ("剤", "ざい", "dose / medicine / drug", ["ザイ", "スイ", "セイ"], []),
        ("洗剤", "せんざい", "detergent / cleanser / cleaning agent / washing material", ["センザイ"], []),
        ("魅する", "みする", "to charm / fascinate / bewitch / enchant", ["ミ"], ["み.する"]),
        ("魅力", "みりょく", "charm / fascination / glamour / attraction / appeal", ["ミリョク"], []),
        ("神秘", "しんぴ", "mystery", ["シンピ"], []),
    ],
    # Lesson 183[cite: 42]
    [
        ("魅力的", "みりょくてき", "charming / fascinating / attractive", ["ミリョクテキ"], []),
        ("契", "けい", "pledge / promise / vow", ["ケイ"], ["ちぎ.る"]),
        ("契機", "けいき", "opportunity / chance / trigger / cause", ["ケイキ"], []),
        ("契約", "けいやく", "contract / compact / agreement", ["ケイヤク"], []),
        ("突破", "とっぱ", "breaking through / breakthrough / penetration", ["トッパ"], []),
    ],
    # Lesson 184[cite: 42]
    [
        ("邪", "じゃ", "wicked / injustice / wrong", ["ジャ"], ["よこし.ま"]),
        ("邪魔", "じゃま", "hindrance / obstacle / nuisance / disturbance", ["ジャマ"], []),
        ("風邪", "かぜ", "common cold / cold / influenza / flu", ["フウジャ"], ["かぜ"]),
        ("風邪を引く", "かぜをひく", "to catch a cold", [], ["かぜをひく"]),
        ("麻酔", "ますい", "anesthesia / anaesthesia", ["マスイ"], []),
    ],
    # Lesson 185[cite: 42]
    [
        ("挑む", "いどむ", "to challenge to (a fight, game, etc.) / throw down the gauntlet", ["チョウ"], ["いど.む"]),
        ("免れる", "まぬがれる", "to escape (disaster, death, etc.) / be saved from / avoid", ["メン"], ["まぬが.れる", "まぬか.れる"]),
        ("無免許", "むめんきょ", "unlicensed / without a license (permit)", ["ムメンキョ"], []),
        ("運転免許証", "うんてんめんきょしょう", "driver's license / driving licence", ["ウンテンメンキョショウ"], []),
        ("挑戦", "ちょうせん", "challenge / defiance / dare / attempt / try", ["チョウセン"], []),
    ],
    # Lesson 186[cite: 42]
    [
        ("択", "たく", "choose / select / elect / prefer", ["タク"], ["えら.ぶ"]),
        ("廊", "ろう", "corridor / hall / tower", ["ロウ"], []),
        ("廊下", "ろうか", "corridor / hallway / passageway", ["ロウカ"], []),
        ("輩", "はい", "comrade / fellow / people / companions", ["ハイ"], ["-ばら", "やから"]),
        ("単", "たん", "simple / one / single / merely", ["タン"], ["ひとえ"]),
    ],
    # Lesson 187[cite: 42]
    [
        ("先輩", "せんぱい", "senior (at work or school) / superior / elder", ["センパイ"], []),
        ("後輩", "こうはい", "junior (at work, school, etc.) / younger people", ["コウハイ"], []),
        ("虚", "きょ", "void / emptiness / unpreparedness / crack / fissure / untruth", ["キョ", "コ"], ["むな.しい", "うつ.ろ"]),
        ("往復", "おうふく", "making a round trip / going and returning / coming and going", ["オウフク"], []),
        ("往", "おう", "journey / travel / chase away / let go / going / before", ["オウ"], ["い.く", "いにしえ", "ゆ.く"]),
    ],
    # Lesson 188[cite: 42]
    [
        ("往復切符", "おうふくきっぷ", "round-trip ticket / return ticket", ["オウフクキップ"], []),
        ("趣", "おもむき", "meaning / tenor / gist / effect / appearance / taste / charm", ["シュ"], ["おもむき", "おもむ.く"]),
        ("趣味", "しゅみ", "hobby / pastime / tastes / preference / liking", ["シュミ"], []),
        ("索", "さく", "cord / rope / searching / lookup", ["サク"], []),
        ("動揺", "どうよう", "shaking / trembling / pitching / rolling / disturbance / unrest", ["ドウヨウ"], []),
    ],
    # Lesson 189[cite: 43]
    [
        ("索引", "さくいん", "index (in a book)", ["サクイン"], []),
        ("模索", "もさく", "groping (for) / searching (for an answer, solution, etc.)", ["モサク"], []),
        ("捜索", "そうさく", "search (esp. for someone or something missing) / manhunt", ["ソウサク"], []),
        ("匂い", "におい", "odour / odor / scent / smell / stench", [], ["にお.い"]),
        ("隣接", "りんせつ", "contiguity / adjacency / bordering", ["リンセツ"], []),
    ],
    # Lesson 190[cite: 43]
    [
        ("匂う", "におう", "to be fragrant / smell (good) / stink / glow", [], ["にお.う"]),
        ("摩", "ま", "chafe / rub / polish / grind / scrape", ["マ"], ["ま.する", "さす.る"]),
        ("滑る", "すべる", "to glide / slide (e.g. on skis) / slip / fail (an exam)", ["カツ", "コツ"], ["すべ.る", "なめ.らか"]),
        ("裸", "はだか", "naked / nude / bare / uncovered", ["ラ"], ["はだか"]),
        ("円滑", "えんかつ", "smooth / undisturbed / uninterrupted / harmonious", ["エンカツ"], []),
    ],
    # Lesson 191[cite: 43]
    [
        ("裸足", "はだし", "barefoot", ["ラソク"], ["はだし"]),
        ("孝", "こう", "filial piety / child's respect", ["コウ", "キョウ"], []),
        ("孝行", "こうこう", "filial piety", ["コウコウ"], []),
        ("綱", "つな", "rope / cord / line", ["コウ"], ["つな"]),
        ("滑らか", "なめらか", "smooth (of a surface) / glassy / velvety / soft", ["カツ"], ["なめ.らか"]),
    ],
    # Lesson 192[cite: 43]
    [
        ("横綱", "よこづな", "yokozuna (highest rank in sumo) / grand champion", [], ["よこづな"]),
        ("邸", "てい", "residence / mansion", ["テイ"], ["やしき"]),
        ("邸宅", "ていたく", "mansion / residence", ["テイタク"], []),
        ("揚げる", "あげる", "to lift / elevate / raise / fry (in deep oil)", ["ヨウ"], ["あ.げる", "あ.がる"]),
        ("尻尾", "しっぽ", "tail (animal)", [], ["しっぽ"]),
    ],
    # Lesson 193[cite: 43]
    [
        ("卓", "たく", "eminent / table / desk / high", ["タク"], []),
        ("食卓", "しょくたく", "dining table", ["ショクタク"], []),
        ("墓", "はか", "grave / tomb", ["ボ"], ["はか"]),
        ("墓地", "ぼち", "cemetery / graveyard", ["ボチ"], []),
        ("旅客", "りょかく", "passenger (transport)", ["リョカク", "リョキャク"], []),
    ],
    # Lesson 194[cite: 43]
    [
        ("耐える", "たえる", "to bear / stand / endure / put up with / support", ["タイ"], ["た.える"]),
        ("臨む", "のぞむ", "to look out on / overlook / face / deal with / attend", ["リン"], ["のぞ.む"]),
        ("臨時", "りんじ", "temporary / special / extraordinary", ["リンジ"], []),
        ("献じる", "けんじる", "to present / dedicate / offer", ["ケン", "コン"], ["けん.じる"]),
        ("臨床", "りんしょう", "clinical (e.g. pathology, psychology)", ["リンショウ"], []),
    ],
    # Lesson 195[cite: 43]
    [
        ("文献", "ぶんけん", "literature / books (reference) / document", ["ブンケン"], []),
        ("献立", "こんだて", "menu / bill of fare / program / schedule", ["コンダテ"], []),
        ("脈", "みゃく", "vein / pulse / hope", ["ミャク"], ["すじ"]),
        ("文脈", "ぶんみゃく", "context", ["ブンミャク"], []),
        ("耐震", "たいしん", "earthquake-proof / quakeproof / seismic", ["タイシン"], []),
    ],
    # Lesson 196[cite: 43]
    [
        ("山脈", "さんみゃく", "mountain range / mountain chain", ["サンミャク"], []),
        ("芝", "しば", "turf / lawn", ["シ"], ["しば"]),
        ("芝居", "しばい", "play / drama", ["シバイ"], []),
        ("芝生", "しばふ", "lawn", [], ["しばふ"]),
        ("交える", "まじえる", "to mix / combine / include / exchange (words, fire)", ["コウ"], ["まじ.える", "ま.じる"]),
    ],
    # Lesson 197[cite: 43]
    [
        ("唱える", "となえる", "to recite / chant / cry / yell / advocate / advance", ["ショウ"], ["とな.える"]),
        ("合唱", "がっしょう", "chorus / singing in a chorus", ["ガッショウ"], []),
        ("誕プレ", "たんプレ", "birthday present", ["タン"], []),
        ("誕生日", "たんじょうび", "birthday", ["タンジョウビ"], []),
        ("育む", "はぐくむ", "to raise / rear / bring up / foster / cultivate", ["イク"], ["はぐく.む"]),
    ],
    # Lesson 198[cite: 43]
    [
        ("貫く", "つらぬく", "to go through / pierce / penetrate / stick to (opinion, principle)", ["カン"], ["つらぬ.く", "ぬ.く"]),
        ("偽", "にせ", "sham / counterfeit / forgery / imitation", ["ギ", "カ"], ["いつわ.る", "にせ"]),
        ("偽物", "にせもの", "spurious article / forgery / counterfeit / imitation / fake", ["ギブツ"], ["にせもの"]),
        ("偽札", "にせさつ", "counterfeit bill / forged banknote", [], ["にせさつ"]),
        ("一貫", "いっかん", "consistency / coherence / integration", ["イッカン"], []),
    ],
    # Lesson 199[cite: 43]
    [
        ("奮う", "ふるう", "to be invigorated / be spirited / flourish", ["フン"], ["ふる.う"]),
        ("桜", "さくら", "cherry tree / cherry blossom", ["オウ", "ヨウ"], ["さくら"]),
        ("熟", "じゅく", "mellow / ripen / mature / acquire skill", ["ジュク"], ["う.れる"]),
        ("熟語", "じゅくご", "kanji compound / idiom / idiomatic phrase", ["ジュクゴ"], []),
        ("興奮", "こうふん", "excitement / stimulation / agitation / arousal", ["コウフン"], []),
    ],
    # Lesson 200[cite: 43]
    [
        ("未熟", "みじゅく", "unripe / green / inexperienced / immature / unskilled", ["ミジュク"], []),
        ("成熟", "せいじゅく", "maturity / ripeness", ["セイジュク"], []),
        ("排", "はい", "repudiate / exclude / expel / reject / line up / arrange", ["ハイ"], []),
        ("排水", "はいすい", "drainage / pumping out water / sewerage", ["ハイスイ"], []),
        ("残高", "ざんだか", "(bank) balance / remainder", ["ザンダカ"], []),
    ],
    # Lesson 201[cite: 44]
    [
        ("排除", "はいじょ", "exclusion / removal / rejection / elimination / ruling out", ["ハイジョ"], []),
        ("透かし", "すかし", "watermark / openwork / transparency", ["トウ"], ["す.かし"]),
        ("棄", "き", "abandon / throw away / discard / resign / reject / sacrifice", ["キ"], ["す.てる"]),
        ("放棄", "ほうき", "abandonment / renunciation / abdication", ["ホウキ"], []),
        ("透明", "とうめい", "transparent / clear", ["トウメイ"], []),
    ],
    # Lesson 202[cite: 44]
    [
        ("棄権", "きけん", "abstention from voting / renunciation of a right", ["キケン"], []),
        ("廃棄", "はいき", "disposal / abandonment / scrapping / annulment", ["ハイキ"], []),
        ("破棄", "はき", "revocation / annulment / cancellation / tearing up", ["ハキ"], []),
        ("削る", "けずる", "to shave (wood or leather) / sharpen / pare / whittle / cut down", ["サク"], ["けず.る"]),
        ("描写", "びょうしゃ", "depiction / description / portrayal", ["ビョウシャ"], []),
    ],
    # Lesson 203[cite: 44]
    [
        ("削除", "さくじょ", "elimination / cancellation / deletion / erasure", ["サクジョ"], []),
        ("奏でる", "かなでる", "to play an instrument (esp. string instruments)", ["ソウ"], ["かな.でる"]),
        ("演奏", "えんそう", "musical performance", ["エンソウ"], []),
        ("麗しい", "うるわしい", "beautiful / lovely / heartwarming", ["レイ"], ["うるわ.しい"]),
        ("弾む", "はずむ", "to spring / bound / bounce / be stimulated / be lively", ["ダン"], ["はず.む", "ひ.く"]),
    ],
    # Lesson 204[cite: 44]
    [
        ("奇麗", "きれい", "pretty / lovely / beautiful / fair / clean / clear / pure", ["キレイ"], []),
        ("逮捕", "たいほ", "arrest / apprehension / capture", ["タイホ"], []),
        ("誠", "まこと", "truth / reality / sincerity / honesty / fidelity", ["セイ"], ["まこと"]),
        ("誠実", "せいじつ", "sincere / honest / faithful", ["セイジツ"], []),
        ("逮", "たい", "apprehend / chase", ["タイ"], []),
    ],
    # Lesson 205[cite: 44]
    [
        ("炎", "ほのお", "flame / blaze", ["エン"], ["ほのお"]),
        ("椅子", "いす", "chair / stool / post / office / position", ["イス"], []),
        ("寛", "かん", "tolerant / leniency / generosity / relax / feel at home / be at ease", ["カン"], ["くつろ.ぐ", "ひろ.い"]),
        ("寛容", "かんよう", "tolerance / open-mindedness / forbearance / generosity", ["カンヨウ"], []),
        ("椅", "い", "chair", ["イ"], []),
    ],
    # Lesson 206[cite: 44]
    [
        ("穂", "ほ", "ear (of plant) / head (of plant) / spike / point / tip", ["スイ"], ["ほ"]),
        ("兼ねて", "かねて", "previously / already / lately / for some time", ["ケン"], ["か.ねて"]),
        ("兼ねる", "かねる", "to be unable to / find difficult (unpleasant, painful) to do / serve two roles", ["ケン"], ["か.ねる"]),
        ("兼用", "けんよう", "multi-use / combined use / combination / serving two purposes", ["ケンヨウ"], []),
        ("懐", "ふところ", "bosom / breast / pocket / purse / heart / feelings", ["カイ", "エ"], ["ふところ", "なつ.かしい"]),
    ],
    # Lesson 207[cite: 44]
    [
        ("兼業", "けんぎょう", "side job / second business / doing two things at once", ["ケンギョウ"], []),
        ("気兼ね", "きがね", "hesitance / diffidence / feeling constraint / fear of troubling someone", [], ["きがね"]),
        ("飼う", "かう", "to keep (a pet or other animal) / have / own / raise / rear", ["シ"], ["か.う"]),
        ("促す", "うながす", "to urge / press / suggest / demand / stimulate / quicken", ["ソク"], ["うなが.す"]),
        ("飼育", "しいく", "breeding / raising / rearing", ["シイク"], []),
    ],
    # Lesson 208[cite: 44]
    [
        ("催促", "さいそく", "pressing / urging / demanding / demand", ["サイソク"], []),
        ("促進", "そくしん", "promotion / acceleration / encouragement / facilitation", ["ソクシン"], []),
        ("彩り", "いろどり", "coloring / colouring / paint / makeup", ["サイ"], ["いろど.り"]),
        ("色彩", "しきさい", "color / colour / hue / tints", ["シキサイ"], []),
        ("利息", "りそく", "interest (on a loan or deposit)", ["リソク"], []),
    ],
    # Lesson 209[cite: 44]
    [
        ("暖かい", "あたたかい", "warm / mild / genial", ["ダン", "ノン"], ["あたた.か", "あたた.かい"]),
        ("暖冬", "だんとう", "mild winter / warm winter", ["ダントウ"], []),
        ("暖房", "だんぼう", "heating", ["ダンボウ"], []),
        ("温暖化", "おんだんか", "warming (e.g. global warming)", ["オンダンカ"], []),
        ("打撃", "だげき", "blow / shock / strike / damage / batting (baseball)", ["ダゲキ"], []),
    ],
    # Lesson 210[cite: 44]
    [
        ("俗", "ぞく", "vulgar / customs / manners / worldliness / mundane things", ["ゾク"], []),
        ("傍ら", "かたわら", "side / edge / beside / besides / while", ["ボウ"], ["かたわ.ら", "わき"]),
        ("肝", "きも", "liver / innards / courage / pluck / nerve / crux", ["カン"], ["きも"]),
        ("肝心", "かんじん", "essential / fundamental / crucial / vital / main", ["カンジン"], []),
        ("施工", "せこう", "construction / carrying out (work)", ["セコウ", "シコウ"], []),
    ],
    # Lesson 211[cite: 44]
    [
        ("畑", "はたけ", "field (for fruits, vegetables, etc.) / cultivated land / vegetable plot", [], ["はた", "はたけ"]),
        ("峰", "みね", "peak / ridge / back of a blade", ["ホウ"], ["みね", "ね"]),
        ("恩", "おん", "grace / kindness / goodness / favor / mercy / blessing / benefit", ["オン"], []),
        ("恩恵", "おんけい", "grace / favor / blessing / benefit", ["オンケイ"], []),
        ("青春", "せいしゅん", "youth / springtime of life / adolescent", ["セイシュン"], []),
    ],
    # Lesson 212[cite: 44]
    [
        ("誇る", "ほこる", "to boast of / be proud of", ["コ"], ["ほこ.る"]),
        ("誇り", "ほこり", "pride / boast", ["コ"], ["ほこ.り"]),
        ("誇張", "こちょう", "exaggeration", ["コチョウ"], []),
        ("網", "あみ", "net / netting", ["モウ"], ["あみ"]),
        ("興味深い", "きょうみぶかい", "very interesting / of great interest", [], ["きょうみぶか.い"]),
    ],
    # Lesson 213[cite: 45]
    [
        ("渋い", "しぶい", "astringent / bitter / puckery / rough / sullen / tasteful / sober", ["ジュウ", "シュウ"], ["しぶ", "しぶ.い"]),
        ("渋谷", "しぶや", "Shibuya (Tokyo)", [], ["しぶや"]),
        ("魂", "たましい", "soul / spirit", ["コン"], ["たましい", "たま"]),
        ("牧", "まき", "breed / care for / shepherd / feed / pasture", ["ボク"], ["まき"]),
        ("染み", "しみ", "stain / blot / spot / smudge / freckle", ["セン"], ["し.み"]),
    ],
    # Lesson 214[cite: 45]
    [
        ("遊牧", "ゆうぼく", "nomadism", ["ユウボク"], []),
        ("牧師", "ぼくし", "pastor / minister / clergyman / reverend", ["ボクシ"], []),
        ("牧場", "ぼくじょう", "farm (livestock) / stock farm / ranch / pasture / meadow", ["ボクジョウ"], ["まきば"]),
        ("控える", "ひかえる", "to be temperate in / refrain / abstain / hold back / jot down", ["コウ"], ["ひか.える"]),
        ("控除", "こうじょ", "subtraction / deduction (e.g. tax)", ["コウジョ"], []),
    ],
    # Lesson 215[cite: 45]
    [
        ("紛れる", "まぎれる", "to be diverted / be distracted / be mistaken for / slip into", ["フン"], ["まぎ.れる", "まぎ.らす"]),
        ("紛らわしい", "まぎらわしい", "confusing / misleading / equivocal / ambiguous", ["フン"], ["まぎ.らわしい"]),
        ("紛失", "ふんしつ", "losing something / loss", ["フンシツ"], []),
        ("紛争", "ふんそう", "dispute / trouble / strife", ["フンソウ"], []),
        ("貧困", "ひんこん", "poverty / penury / need / destitution", ["ヒンコン"], []),
    ],
    # Lesson 216[cite: 45]
    [
        ("戒め", "いましめ", "caution / admonition / warning / lesson / commandment", ["カイ"], ["いまし.め"]),
        ("警戒", "けいかい", "vigilance / caution / alertness / precaution / guard", ["ケイカイ"], []),
        ("没", "ぼつ", "drown / sink / hide / fall into / disappear / die", ["ボツ", "モツ"], ["おぼ.れる", "しず.む"]),
        ("沈没", "ちんぼつ", "sinking / foundering / going down / getting dead drunk", ["チンボツ"], []),
        ("英雄", "えいゆう", "hero / heroine / great person", ["エイユウ"], []),
    ],
    # Lesson 217[cite: 45]
    [
        ("没落", "ぼつらく", "ruin / fall / collapse / downfall / bankruptcy", ["ボツラク"], []),
        ("没収", "ぼっしゅう", "forfeiture / seizure / confiscation / impoundment", ["ボッシュウ"], []),
        ("既に", "すでに", "already / too late", ["キ"], ["すで.に"]),
        ("既婚", "きこん", "married / marriage", ["キコン"], []),
        ("水田", "すいでん", "paddy field / water-filled paddy field", ["スイデン"], []),
    ],
    # Lesson 218[cite: 45]
    [
        ("股", "また", "groin / crotch / thigh / fork (in a tree, road, etc.)", ["コ"], ["また", "もも"]),
        ("脅す", "おどす", "to threaten / menace / frighten (into doing)", ["キョウ"], ["おびや.かす", "おど.す"]),
        ("脅かす", "おびやかす", "to intimidate / threaten / menace / endanger", ["キョウ"], ["おびや.かす"]),
        ("脅迫", "きょうはく", "threat / menace / coercion / blackmail", ["キョウハク"], []),
        ("土木", "どぼく", "engineering works / civil engineering / public works", ["ドボク"], []),
    ],
    # Lesson 219[cite: 45]
    [
        ("征", "せい", "subjugate / attack the rebellious / collect taxes", ["セイ"], []),
        ("征服", "せいふく", "conquest / subjugation / overcoming", ["セイフク"], []),
        ("覆す", "くつがえす", "to overturn / capsize / upset / overthrow (government)", ["フク"], ["くつがえ.す"]),
        ("覆う", "おおう", "to cover / hide / conceal / wrap / disguise", ["フク"], ["おお.う", "くつがえ.す"]),
        ("発作", "ほっさ", "fit / spasm / attack / seizure / paroxysm", ["ホッサ"], []),
    ],
    # Lesson 220[cite: 45]
    [
        ("覆面", "ふくめん", "mask / veil / disguise", ["フクメン"], []),
        ("郡", "ぐん", "county / district", ["グン"], ["こおり"]),
        ("丘", "おか", "hill / height / knoll / rising ground", ["キュウ"], ["おか"]),
        ("佳", "か", "excellent / beautiful / good / pleasing / skilled", ["カ"], []),
        ("費やす", "ついやす", "to spend / expend / consume / waste (time, money, etc.)", ["ヒ"], ["つい.やす", "つい.える"]),
    ],
    # Lesson 221[cite: 45]
    [
        ("佳句", "かく", "good phrase / fine passage / beautiful line of poetry", ["カク"], []),
        ("叔父", "おじ", "uncle (younger than one's parent)", ["シュクフ"], ["おじ"]),
        ("叔母", "おば", "aunt (younger than one's parent)", ["シュクボ"], ["おば"]),
        ("託す", "たくす", "to entrust (someone) with / leave (a matter) with / use as a pretext", ["タク"], ["たく.す", "かこつ.ける"]),
        ("叔", "しゅく", "uncle / youth", ["シュク"], []),
    ],
    # Lesson 222[cite: 45]
    [
        ("委託", "いたく", "entrusting (to someone) / consignment / commission", ["イタク"], []),
        ("哀れ", "あわれ", "pity / sorrow / grief / misery / compassion / pathos", ["アイ"], ["あわ.れ", "あわ.れむ"]),
        ("可哀想", "かわいそう", "poor / pitiable / pathetic / pitiful", ["カアイソウ"], []),
        ("肥", "ひ", "fertilizer / get fat / fertile / manure / pamper", ["ヒ"], ["こ.える", "こえ"]),
        ("埋まる", "うまる", "to be buried / be covered / be surrounded / overflow / be filled", ["マイ"], ["う.まる", "うず.まる"]),
    ],
    # Lesson 223[cite: 45]
    [
        ("肥料", "ひりょう", "manure / fertilizer / fertiliser / compost", ["ヒリョウ"], []),
        ("朗らか", "ほがらか", "bright / cheerful / melodious / clear (sky)", ["ロウ"], ["ほが.らか"]),
        ("慎む", "つつしむ", "to be careful / be discreet / do in moderation / refrain", ["シン"], ["つつし.む", "つつし.み"]),
        ("慎重", "しんちょう", "discretion / prudence / caution / care", ["シンチョウ"], []),
        ("空しい", "むなしい", "vacant / futile / vain / void / empty / ineffective", ["クウ"], ["むな.しい"]),
    ],
    # Lesson 224[cite: 45]
    [
        ("眉", "まゆ", "eyebrow", ["ビ", "ミ"], ["まゆ"]),
        ("眉毛", "まゆげ", "eyebrows", [], ["まゆげ"]),
        ("拒む", "こばむ", "to refuse / reject / decline / rebuff", ["キョ", "ゴ"], ["こば.む"]),
        ("拒絶", "きょぜつ", "refusal / rejection", ["キョゼツ"], []),
        ("尋問", "じんもん", "questioning / interrogation / examination", ["ジンモン"], []),
    ],
    # Lesson 225[cite: 45]
    [
        ("拒否", "きょひ", "refusal / rejection / denial / veto", ["キョヒ"], []),
        ("概して", "がいして", "generally / as a rule", ["ガイ"], []),
        ("概説", "がいせつ", "general statement / outline / summary", ["ガイセツ"], []),
        ("概論", "がいろん", "introduction / outline / general remarks", ["ガイロン"], []),
        ("概ね", "おおむね", "in general / mainly / roughly / approximately", ["ガイ"], ["おおむ.ね"]),
    ],
    # Lesson 226[cite: 46]
    [
        ("概念", "がいねん", "general idea / concept / notion", ["ガイネン"], []),
        ("大概", "たいがい", "generally / usually / mostly / probably", ["タイガイ"], []),
        ("概略", "がいりゃく", "outline / summary / gist / in brief", ["ガイリャク"], []),
        ("一概に", "いちがいに", "unconditionally / as a whole / sweepingly", ["イチガイ"], []),
        ("下請け", "したうけ", "subcontract / subcontractor", [], ["したうけ"]),
    ],
    # Lesson 227[cite: 46]
    [
        ("顧みる", "かえりみる", "to look back / turn around / look back upon / review", ["コ"], ["かえり.みる"]),
        ("腐る", "くさる", "to rot / go bad / decay / spoil / corrode", ["フ"], ["くさ.る", "くさ.れる"]),
        ("挨拶", "あいさつ", "greeting / greetings / salutation / polite set phrase", ["アイサツ"], []),
        ("却", "きゃく", "instead / on the contrary / rather / step back / withdraw", ["キャク"], ["かえ.って", "しりぞ.く"]),
        ("拶", "さつ", "be imminent / draw close", ["サツ"], ["せま.る"]),
    ],
    # Lesson 228[cite: 46]
    [
        ("返却", "へんきゃく", "return of something / repayment", ["ヘンキャク"], []),
        ("荘", "そう", "villa / inn / cottage / feudal manor / solemn / dignified", ["ソウ", "ショウ", "チャン"], ["ほうき", "おごそ.か"]),
        ("別荘", "べっそう", "holiday house / vacation home / villa", ["ベッソウ"], []),
        ("悔しい", "くやしい", "vexing / annoying / frustrating / regrettable / mortifying", ["カイ"], ["くや.しい", "くや.む"]),
        ("顧客", "こきゃく", "customer / client / patron", ["コキャク", "コカク"], []),
    ],
    # Lesson 229[cite: 46]
    [
        ("後悔", "こうかい", "regret / repentance / remorse", ["コウカイ"], []),
        ("獄", "ごく", "prison / jail", ["ゴク"], []),
        ("地獄", "じごく", "hell", ["ジゴク"], []),
        ("滞る", "とどこおる", "to stagnate / be delayed / be overdue / fall into arrears", ["タイ"], ["とどこお.る"]),
        ("豆腐", "とうふ", "tofu / bean curd", ["トウフ"], []),
    ],
    # Lesson 230[cite: 46]
    [
        ("渋滞", "じゅうたい", "congestion (e.g. traffic) / delay / stagnation", ["ジュウタイ"], []),
        ("滞在", "たいざい", "stay / sojourn", ["タイザイ"], []),
        ("遇す", "ぐうす", "to treat / handle / deal with / entertain", ["グウ"], ["ぐう.す"]),
        ("境遇", "きょうぐう", "environment / circumstances / situation", ["キョウグウ"], []),
        ("落下", "らっか", "fall / drop / descent", ["ラッカ"], []),
    ],
    # Lesson 231[cite: 46]
    [
        ("待遇", "たいぐう", "treatment / reception / service / working conditions / pay", ["タイグウ"], []),
        ("淡水", "たんすい", "fresh water (i.e. not salt water)", ["タンスイ"], []),
        ("冷淡", "れいたん", "cool / indifferent / apathetic / half-hearted / cold-hearted", ["レイタン"], []),
        ("購", "こう", "subscription / buy", ["コウ"], []),
        ("淡", "たん", "thin / faint / pale / fleeting", ["タン"], ["あわ.い"]),
    ],
    # Lesson 232[cite: 46]
    [
        ("購買", "こうばい", "procurement / purchase / buying", ["コウバイ"], []),
        ("購入", "こうにゅう", "purchase / buy", ["コウニュウ"], []),
        ("購読", "こうどく", "paid subscription (e.g. magazine)", ["コウドク"], []),
        ("崇める", "あがめる", "to revere / respect / worship / admire", ["スウ"], ["あが.める"]),
        ("淡い", "あわい", "light / faint / pale / fleeting", ["タン"], ["あわ.い"]),
    ],
    # Lesson 233[cite: 46]
    [
        ("崇拝", "すうはい", "worship / adoration / admiration / cult", ["スウハイ"], []),
        ("唯", "ゆい", "solely / only / merely / simply", ["ユイ", "イ"], ["ただ"]),
        ("唯一", "ゆいいつ", "only / sole / unique", ["ユイイツ"], []),
        ("垂れる", "たれる", "to hang / droop / dangle / sag / drip / ooze", ["スイ"], ["た.れる", "た.らす"]),
        ("連なる", "つらなる", "to extend / stretch out / stand in a row / attend", ["レン"], ["つら.なる", "つら.ねる"]),
    ],
    # Lesson 234[cite: 46]
    [
        ("垂直", "すいちょく", "vertical / perpendicular", ["スイチョク"], []),
        ("俳優", "はいゆう", "actor / actress / player / performer", ["ハイユウ"], []),
        ("斜め", "ななめ", "slanting / tilted / sloping / diagonal / oblique", ["シャ"], ["なな.め", "はす"]),
        ("嬢", "じょう", "lass / girl / Miss / daughter", ["ジョウ"], ["むすめ"]),
        ("俳", "はい", "haiku / actor", ["ハイ"], []),
    ],
    # Lesson 235[cite: 46]
    [
        ("お嬢さん", "おじょうさん", "(another's) daughter / young lady", ["ジョウ"], ["おじょうさん"]),
        ("陥る", "おちいる", "to fall into (e.g. a hole) / fall into (chaos, depression, dilemma)", ["カン"], ["おちい.る", "おとしい.れる"]),
        ("償い", "つぐない", "atonement / compensation / indemnity", ["ショウ"], ["つぐな.い"]),
        ("弁償", "べんしょう", "compensation / reparation / indemnity / reimbursement", ["ベンショウ"], []),
        ("斜面", "しゃめん", "slope / slanting surface / bevel", ["シャメン"], []),
    ],
    # Lesson 236[cite: 46]
    [
        ("補償", "ほしょう", "compensation / reparation", ["ホショウ"], []),
        ("鑑", "かがみ", "specimen / take warning from / learn from", ["カン"], ["かんが.みる", "かがみ"]),
        ("印鑑", "いんかん", "stamp / seal", ["インカン"], []),
        ("勧める", "すすめる", "to recommend (someone to do) / advise / encourage / offer", ["カン", "ケン"], ["すす.める"]),
        ("勧告", "かんこく", "advice / counsel / remonstrance / recommendation", ["カンコク"], []),
    ],
    # Lesson 237[cite: 46]
    [
        ("葬る", "ほうむる", "to bury / inter / entomb / hush up / shelve", ["ソウ"], ["ほうむ.る"]),
        ("葬式", "そうしき", "funeral", ["ソウシキ"], []),
        ("焦る", "あせる", "to be in a hurry / be impatient / be anxious / fret", ["ショウ"], ["あせ.る"]),
        ("焦り", "あせり", "impatience", ["ショウ"], ["あせ.り"]),
        ("焦点", "しょうてん", "focus (e.g. photographic) / focal point", ["ショウテン"], []),
    ],
    # Lesson 238[cite: 47]
    [
        ("焦げる", "こげる", "to burn / scorch / singe / char", ["ショウ"], ["こ.げる", "こ.がす"]),
        ("膨らむ", "ふくらむ", "to expand / swell (out) / get big / become inflated", ["ボウ"], ["ふく.らむ", "ふく.れる"]),
        ("膨れる", "ふくれる", "to swell (out) / expand / be inflated / distend / bulge", ["ボウ"], ["ふく.れる", "ふく.らむ"]),
        ("膨らます", "ふくらます", "to swell / expand / inflate / bulge", ["ボウ"], ["ふく.らます"]),
        ("欠陥", "けっかん", "defect / fault / deficiency / deformity / shortage", ["ケッカン"], []),
    ],
    # Lesson 239[cite: 47]
    [
        ("膨大", "ぼうだい", "huge / vast / enormous / colossal / extensive", ["ボウダイ"], []),
        ("紫", "むらさき", "purple / violet", ["シ"], ["むらさき"]),
        ("鎌倉", "かまくら", "Kamakura", [], ["かまくら"]),
        ("菌", "きん", "germ / fungus / bacteria", ["キン"], []),
        ("倉", "くら", "godown / warehouse / storehouse / cellar / treasury", ["ソウ"], ["くら"]),
    ],
    # Lesson 240[cite: 47]
    [
        ("細菌", "さいきん", "bacterium / bacteria / germ", ["サイキン"], []),
        ("稼ぐ", "かせぐ", "to earn (income) / make (money) / score (points, victory)", ["カ"], ["かせ.ぐ"]),
        ("譲る", "ゆずる", "to hand over / transfer / turn over / assign / convey / bequeath", ["ジョウ"], ["ゆず.る"]),
        ("随", "ずい", "follow / though / notwithstanding / while / during / both", ["ズイ"], ["まにま.に", "したが.う"]),
        ("随分", "ずいぶん", "very / extremely / surprisingly / considerably / awfully", ["ズイブン"], []),
    ],
    # Lesson 241[cite: 47]
    [
        ("遂に", "ついに", "finally / at last / in the end", ["スイ"], ["つい.に"]),
        ("遂げる", "とげる", "to accomplish / achieve / carry out", ["スイ"], ["と.げる"]),
        ("やり遂げる", "やりとげる", "to accomplish / finish / carry through", [], ["やりと.げる"]),
        ("冒す", "おかす", "to brave / risk / face / venture / defy / desecrate", ["ボウ"], ["おか.す"]),
        ("譲渡", "じょうと", "transfer / assignment / conveyance", ["ジョウト"], []),
    ],
    # Lesson 242[cite: 47]
    [
        ("冒険", "ぼうけん", "adventure / venture", ["ボウケン"], []),
        ("冒頭", "ぼうとう", "beginning / start / outset", ["ボウトウ"], []),
        ("翼", "つばさ", "wing", ["ヨク"], ["つばさ"]),
        ("凄い", "すごい", "terrible / dreadful / amazing / great / wonderful / to a great extent", ["セイ"], ["すご.い"]),
        ("遂行", "すいこう", "accomplishment / execution / performance / carrying out", ["スイコウ"], []),
    ],
    # Lesson 243[cite: 47]
    [
        ("物凄い", "ものすごい", "earth-shattering / staggering / to a very great extent", [], ["ものすご.い"]),
        ("序", "じょ", "preface / beginning / order / precedence / occasion / chance", ["ジョ"], ["つい.で", "ついで"]),
        ("順序", "じゅんじょ", "order / sequence / procedure", ["ジュンジョ"], []),
        ("倉庫", "そうこ", "storehouse / warehouse / godown", ["ソウコ"], []),
        ("凄まじい", "すさまじい", "terrific / fierce / terrible / tremendous / dreadful / awful", ["セイ"], ["すさ.まじい"]),
    ],
    # Lesson 244[cite: 47]
    [
        ("扉", "とびら", "door / gate / opening / title page", ["ヒ"], ["とびら"]),
        ("是", "ぜ", "just so / this / right / justice", ["ゼ", "シ"], ["これ"]),
        ("是非", "ぜひ", "certainly / without fail / right and wrong / pros and cons", ["ゼヒ"], []),
        ("是非とも", "ぜひとも", "by all means (with sense of not taking 'no' for an answer)", ["ゼヒ"], []),
        ("静脈", "じょうみゃく", "vein", ["ジョウミャク"], []),
    ],
    # Lesson 245[cite: 47]
    [
        ("バス賃", "バスちん", "bus fare", ["チン"], []),
        ("家賃", "やちん", "rent", ["ヤチン"], []),
        ("澄む", "すむ", "to become clear (water, air, etc.) / become transparent / resonate clearly", ["チョウ"], ["す.む", "す.ます"]),
        ("澄ます", "すます", "to clear / make clear / strain (one's ears) / look unconcerned", ["チョウ"], ["す.ます"]),
        ("賃金", "ちんぎん", "wages", ["チンギン"], []),
    ],
    # Lesson 246[cite: 47]
    [
        ("殊に", "ことに", "especially / above all", ["シュ"], ["こと"]),
        ("特殊", "とくしゅ", "special / particular / peculiar / unique", ["トクシュ"], []),
        ("緩い", "ゆるい", "loose / slack / gentle (slope) / slow (speed) / lenient", ["カン"], ["ゆる.い", "ゆる.やか"]),
        ("頑な", "かたくな", "obstinate / stubborn", ["ガン"], ["かたくな"]),
        ("緩和", "かんわ", "relief / mitigation / alleviation / relaxation (of restrictions)", ["カンワ"], []),
    ],
    # Lesson 247[cite: 47]
    [
        ("頑張る", "がんばる", "to persevere / persist / keep at it / hang on / hold out / do one's best", ["ガン"], ["がんば.る"]),
        ("糖", "とう", "sugar", ["トウ"], []),
        ("砂糖", "さとう", "sugar", ["サトウ"], []),
        ("煮る", "にる", "to boil / simmer / stew / seethe", ["シャ"], ["に.る", "に.える"]),
        ("賃貸", "ちんたい", "lease / rental", ["チンタイ"], []),
    ],
    # Lesson 248[cite: 47]
    [
        ("惨め", "みじめ", "miserable / wretched / unhappy / sad / pitiable", ["サン", "ザン"], ["みじ.め"]),
        ("悲惨", "ひさん", "disastrous / tragic / miserable / wretched / pitiful", ["ヒサン"], []),
        ("歓", "かん", "delight / joy", ["カン"], ["よろこ.ぶ"]),
        ("歓迎", "かんげい", "welcome / reception", ["カンゲイ"], []),
        ("勝る", "まさる", "to excel / surpass / exceed / have an edge / be superior", ["ショウ"], ["まさ.る", "か.つ"]),
    ],
    # Lesson 249[cite: 47]
    [
        ("歓迎会", "かんげいかい", "welcome party", ["カンゲイカイ"], []),
        ("喉", "のど", "throat / singing voice", ["コウ"], ["のど"]),
        ("旨", "むね", "purport / principle / command / intention", ["シ"], ["むね", "うま.い"]),
        ("趣旨", "しゅし", "object / meaning / gist / point / aim / intent", ["シュシ"], []),
        ("旨い", "うまい", "delicious / appetizing / sweet / skillful / clever / fortunate", ["シ"], ["うま.い"]),
    ],
    # Lesson 250[cite: 47]
    [
        ("要旨", "ようし", "gist / essentials / summary / fundamentals", ["ヨウシ"], []),
        ("凝る", "こる", "to grow stiff / become absorbed in / devote oneself to / be elaborate", ["ギョウ"], ["こ.る", "こ.らす"]),
        ("凝らす", "こらす", "to concentrate / devote / strain / rack (one's brains)", ["ギョウ"], ["こ.らす"]),
        ("圏", "けん", "sphere / circle / radius / range", ["ケン"], ["かこ.い"]),
        ("念仏", "ねんぶつ", "Nenbutsu (Buddhist invocation) / chanting the name of Amida Buddha", ["ネンブツ"], []),
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
    if not os.path.exists(PART1_JSON_PATH):
        raise FileNotFoundError(f"Run 'python generate_n1_part1.py' first to create {PART1_JSON_PATH}.")

    with open(PART1_JSON_PATH, "r", encoding="utf-8") as f:
        lessons = json.load(f)

    item_counter = sum(len(l["items"]) for l in lessons) + 1

    for l_idx, chunk in enumerate(N1_PART2_DATA):
        lesson_num = 126 + l_idx
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

    with open(PART2_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(lessons, f, ensure_ascii=False)

    print(f"Part 2 complete! Saved Lessons 1-250 ({item_counter - 1} items) to {PART2_JSON_PATH}.")


if __name__ == "__main__":
    main()