# Critic evidence: local Kokoro af_river (speed 1.0) vs River

River reference: median F0 210 Hz over 14 shipped sentence clips.

## A. 60-clip sample (local only)

| # | key | lvl | kind | sec | chars/s | F0 | cos->River | WER | whisper small.en | text | extra |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | ipa:ɡˈɪlt | 2 | word | 0.66 | 6.1 | 176 | 0.72 | 0.0 | They guilt. | gilt | phoneme-recogniser PER 0.0 heard 'ɡɪlt' |
| 2 | ipa:swˈit | 3 | word | 0.63 | 7.9 | 176 | 0.56 | 1.0 | So, that was weird. | sweet | phoneme-recogniser PER 0.75 heard 'aswed' |
| 3 | w:mall | 4 | word | 0.62 | 6.5 | 174 | 0.68 | 1.0 | ZAIO! MALI! | mall | phoneme-recogniser PER 0.67 heard 'ma' |
| 4 | ipa:dɹˈʌɡ | 2 | word | 0.67 | 6.0 | 177 | 0.64 | 0.0 | They drug it. | drug | phoneme-recogniser PER 1.0 heard 'dɹɑɡiɛɜ' |
| 5 | w:blue | 3 | word | 0.64 | 6.2 | 177 | 0.85 | 0.0 | they blew it | blue | phoneme-recogniser PER 0.33 heard 'bluɛ' |
| 6 | w:runs | 4 | word | 0.76 | 5.3 | 180 | 0.75 | 0.0 | They... runs... | runs | phoneme-recogniser PER 0.0 heard 'ɹʌnz' |
| 7 | ipa:wˈip | 2 | word | 0.65 | 6.2 | 186 | 0.46 | 1.0 | So, we're back. | weep | phoneme-recogniser PER 1.33 heard 'wei5pa5' |
| 8 | w:snail | 3 | word | 0.66 | 7.6 | 177 | 0.81 | 0.0 | Say snail. | snail | phoneme-recogniser PER 0.5 heard 'sneɪʌll' |
| 9 | w:seven | 4 | word | 0.57 | 8.8 | 173 | 0.83 | 0.0 | So, 7. | seven | phoneme-recogniser PER 0.0 heard 'sɛvʌn' |
| 10 | ipa:mˈæsk | 2 | word | 0.65 | 6.2 | 176 | 0.60 | 0.0 | Say, Mask. | mask | phoneme-recogniser PER 0.0 heard 'mæsk' |
| 11 | ipa:bɹˈɪŋ | 3 | word | 0.69 | 7.2 | 182 | 0.50 | 0.0 | they bring | bring | phoneme-recogniser PER 0.5 heard 'bɹʌaɪ' |
| 12 | w:spreads | 4 | word | 0.75 | 9.3 | 176 | 0.85 | 0.0 | So spreads. | spreads | phoneme-recogniser PER 0.33 heard 'ʌsbɹɛdz' |
| 13 | w:chop | 2 | word | 0.56 | 7.1 | 175 | 0.66 | 1.0 | their job | chop | phoneme-recogniser PER 0.67 heard 'dʒɑb' |
| 14 | ipa:tˈæb | 3 | word | 0.6 | 5.0 | 163 | 0.69 | 0.0 | ZA-TAB | tab | phoneme-recogniser PER 0.33 heard 'tab' |
| 15 | ipa:fˈaɪtɪŋ | 4 | word | 0.8 | 10.0 | 184 | 0.53 | 0.0 | They fighting. | fighting | phoneme-recogniser PER 0.0 heard 'faɪtɪŋ' |
| 16 | w:squid | 2 | word | 0.68 | 7.4 | 166 | 0.70 | 1.0 | So, squared. | squid | phoneme-recogniser PER 0.6 heard 'askwɛdʌ' |
| 17 | ipa:pˈeɪl | 3 | word | 0.64 | 6.2 | 179 | 0.76 | 0.0 | They pale. | pale | phoneme-recogniser PER 0.33 heard 'peɪ' |
| 18 | w:chasing | 4 | word | 0.84 | 8.3 | 187 | 0.78 | 1.0 | So, choosing... | chasing | phoneme-recogniser PER 0.6 heard 'tʃɑjzɪŋ' |
| 19 | read:L2.07:A:0 | 2 | sentence | 13.57 | 19.7 | 168 | 0.89 | 0.0 | Dad and Min set up a tent on the sand. Min helps Dad pull the tent up. | Dad and Min set up a tent on the sand. Min helps Dad pull the tent up. |  |
| 20 | t2:L3.04:0 | 3 | sentence | 3.73 | 20.1 | 175 | 0.91 | 0.0 | Routine. Routine means a set of steps you do the same way again and ag | routine. Routine means a set of steps you do the same way, again and a |  |
| 21 | read:L4.06:B:5 | 4 | sentence | 3.87 | 21.2 | 176 | 0.90 | 0.0 | Someone found a radio and is counting down the minutes until the power | Someone found a radio and is counting down the minutes until the power |  |
| 22 | read:L2.03:A:0 | 2 | sentence | 1.63 | 17.8 | 191 | 0.83 | 0.143 | Men and Dad were at the bath. | Min and Dad were at the bath. |  |
| 23 | t2:L3.16:0 | 3 | sentence | 3.57 | 21.0 | 181 | 0.92 | 0.0 | Daunting. Daunting means something that feels big and a bit scary to s | daunting. Daunting means something that feels big and a bit scary to s |  |
| 24 | read:L4.12:B:1 | 4 | sentence | 5.53 | 19.9 | 175 | 0.91 | 0.0 | It is a simple place, one room, a basket for firewood and a helmet han | It is a simple place — one room, a basket for firewood, and a helmet h |  |
| 25 | read:L2.08:B:0 | 2 | sentence | 13.67 | 19.8 | 166 | 0.89 | 0.0 | Who could help scrub the shop? Sam's boss asks. I could, Sam says and  | "Who could help scrub the shop?" Sam's boss asks. "I could," Sam says, |  |
| 26 | read:L3.12:A:0 | 3 | sentence | 14.36 | 20.9 | 168 | 0.94 | 0.0 | Sam and his dad walk to the pond with a fine boat. When snow starts th | Sam and his dad walk to the pond with a fine boat. When snow starts, t |  |
| 27 | read:L4.06:A:2 | 4 | sentence | 3.41 | 20.5 | 176 | 0.85 | 0.0 | Then a clown in a big gown and a bright crown came by honking a horn. | Then a clown in a big gown and a bright crown came by, honking a horn. |  |
| 28 | read:L2.01:B:4 | 2 | sentence | 2.5 | 18.8 | 182 | 0.93 | 0.0 | It is on the shelf, not in his bag, Sam says. | "It is on the shelf, not in his bag," Sam says. |  |
| 29 | read:L3.08:B:0 | 3 | sentence | 15.86 | 18.9 | 171 | 0.92 | 0.0 | Kate got a job at the market. She helps at a cart that sells fresh gra | Kate got a job at the market. She helps at a cart that sells fresh gra |  |
| 30 | read:L4.14:B:0 | 4 | sentence | 3.57 | 19.0 | 177 | 0.89 | 0.0 | At the office, the internet has been nonstop unreliable all morning. | At the office, the internet has been nonstop unreliable all morning. |  |
| 31 | read:L2.13:A:0 | 2 | sentence | 23.75 | 12.6 | 168 | 0.94 | 0.0 | Men and dad go to visit a friend. They pack a backpack with a napkin a | Min and Dad go to visit a friend. They pack a backpack with a napkin a |  |
| 32 | t2:L3.10:0 | 3 | sentence | 3.69 | 19.5 | 177 | 0.89 | 0.0 | Temporary. Temporary means lasting only for a short time, not permanen | temporary. Temporary means lasting only for a short time, not permanen |  |
| 33 | lt:L2.11:0 | 2 | passage | 10.84 | 20.8 | 172 | 0.93 | 0.027 | The night before her first big exam, Aisha felt more anxious than she  | The night before her first big exam, Ayesha felt more anxious than she |  |
| 34 | lt:L3.04:0 | 3 | passage | 10.27 | 19.1 | 166 | 0.94 | 0.0 | A shopkeeper's closing routine matters because a rushed close can leav | A shopkeeper's closing routine matters because a rushed close can leav |  |
| 35 | lt:L4.02:0 | 4 | passage | 9.55 | 18.1 | 170 | 0.94 | 0.0 | Long before cars, people used horses to travel. A caravan was a group  | Long before cars, people used horses to travel. A caravan was a group  |  |
| 36 | lt:L2.03:2 | 2 | passage | 6.42 | 19.8 | 177 | 0.92 | 0.0 | I borrowed them to fix my bike, Grandpa, I forgot to tell you," she sa | "I borrowed them to fix my bike, Grandpa — I forgot to tell you!" she  |  |
| 37 | lt:L3.06:0 | 3 | passage | 11.7 | 19.8 | 168 | 0.92 | 0.0 | A customer who takes the time to leave a kind note is showing genuine  | A customer who takes the time to leave a kind note is showing genuine  |  |
| 38 | lt:L4.08:0 | 4 | passage | 8.71 | 19.6 | 170 | 0.94 | 0.0 | When someone stays calm and keeps making good choices even after somet | When someone stays calm and keeps making good choices even after somet |  |
| 39 | lt:L2.02:0 | 2 | passage | 6.6 | 20.3 | 171 | 0.93 | 0.0 | A little cat named Pip was very curious. Every single day, Pip wanted  | A little cat named Pip was very curious. Every single day, Pip wanted  |  |
| 40 | lt:L3.09:0 | 3 | passage | 11.68 | 18.8 | 166 | 0.95 | 0.0 | Before horses could be domesticated for riding, humans had to build a  | Before horses could be domesticated for riding, humans had to build a  |  |
| 41 | lt:L4.05:0 | 4 | passage | 7.88 | 19.8 | 171 | 0.92 | 0.0 | When people work well together and things go smoothly, we sometimes sa | When people work well together and things go smoothly, we sometimes sa |  |
| 42 | lt:L2.04:2 | 2 | passage | 10.63 | 21.5 | 168 | 0.91 | 0.025 | Finally, her grandmother sat beside her and said, When you are puzzled | Finally, her grandmother sat beside her and said, "When you are puzzle |  |
| 43 | rule:L2.06 | 2 | instruction | 10.58 | 19.0 | 169 | 0.91 | 0.0 | Blends two consonants side by side keep both sounds. Say them quickly  | Blends. Two consonants side by side keep BOTH sounds. Say them quickly |  |
| 44 | rule:L3.03 | 3 | instruction | 3.4 | 18.8 | 183 | 0.89 | 0.286 | Silent EO, you and E work the same way. Hop Hope Cub Cube. | Silent e. oe, ue and ee work the same way: hop, hope; cub, cube. |  |
| 45 | ui:attackVowels | 4 | instruction | 1.6 | 13.8 | 175 | 0.91 | 0.0 | Tap every vowel sound. | Tap every vowel sound. |  |
| 46 | rule:L2.12 | 2 | instruction | 6.88 | 20.8 | 169 | 0.93 | 0.0 | Two syllable words find the two vowels. Split between the two consonan | Two-syllable words. Find the two vowels. Split between the two consona |  |
| 47 | rule:L3.05 | 3 | instruction | 6.8 | 18.4 | 168 | 0.95 | 0.16 | Open syllables. A syllable that ends with a vowel is open. The vowel s | Open syllables. A syllable that ends with a vowel is open: the vowel s |  |
| 48 | ui:teachSuffix | 4 | instruction | 2.95 | 20.0 | 175 | 0.91 | 0.0 | This is an ending. Read the base word, then add the ending. | This is an ending. Read the base word, then add the ending. |  |
| 49 | rule:L2.08 | 2 | name | 7.26 | 16.7 | 177 | 0.91 | 0.25 | 3-letter blends, S plus a blend, 3 sounds said quickly SDR and strap.  | Three-letter blends. s plus a blend: three sounds said quickly, s-t-r  |  |
| 50 | rule:L3.07 | 3 | name | 8.02 | 16.6 | 171 | 0.89 | 0.103 | Soft C and soft G before E, I or Y, C says S and G usually says J. Cit | Soft c and soft g. Before e, i or y, c says /s/ and g usually says /j/ |  |
| 51 | read:L4.10:B:4 | 4 | name | 10.94 | 20.8 | 172 | 0.93 | 0.0 | It was a simple fix, Bilal tells the customer when she comes to collec | "It was a simple fix," Bilal tells the customer when she comes to coll |  |
| 52 | ss:L5.13:warm:w5 | 5 | name | 0.61 | 6.6 | 169 | 0.48 | 1.0 | Next | dict | OOV overridden: dict |
| 53 | ss:L6.15:text:0:4 | 6 | name | 34.84 | 8.6 | 166 | 0.94 | 0.011 | In 1857, a major uprising against Company Rule broke out, involving so | In 1857, a major uprising against Company rule broke out, involving so | OOV overridden: Mughal,Babur |
| 54 | ss:L7.04:text:0:3 | 7 | name | 43.01 | 7.0 | 168 | 0.95 | 0.023 | On the no-phone nights, the average participant fell asleep nine minut | On the "no phone" nights, the average participant fell asleep 9 minute | OOV overridden: GlowGuard's |
| 55 | ss:L5.07:word:7:m | 5 | sentence | 2.11 | 16.6 | 184 | 0.92 | 0.0 | Celebration, the act of celebrating. | celebration: the act of celebrating |  |
| 56 | ss:L6.09:flu:0 | 6 | passage | 14.71 | 20.4 | 166 | 0.94 | 0.0 | Before you believe anything you read online, ask one simple question.  | Before you believe anything you read online, ask one simple question:  |  |
| 57 | ss:L7.07:disc:2 | 7 | sentence | 6.79 | 21.8 | 172 | 0.93 | 0.0 | Explain the difference between this essay commits fallacies and this e | Explain the difference between "this essay commits fallacies" and "thi |  |
| 58 | ss:L5.12:word:2:m | 5 | sentence | 2.12 | 17.5 | 188 | 0.87 | 0.0 | Superpower, a power beyond the normal. | superpower: a power beyond the normal |  |
| 59 | ss:L6.01:disc:0 | 6 | sentence | 3.24 | 18.8 | 180 | 0.89 | 0.111 | Roll to the learner for paragraph 3, the tissues paragraph. | Role to the learner for paragraph 3 (the tissues paragraph):. |  |
| 60 | ss:L7.14:prime:q | 7 | passage | 8.91 | 22.0 | 172 | 0.92 | 0.0 | Think of the last time you had to read something long and dense. A man | think of the last time you had to read something long and dense (a man |  |

## B. Twins: same item, local vs shipped River
| key | text | local sec | River sec | local F0 | River F0 | cos(local,River) | local whisper |
|---|---|---|---|---|---|---|---|
| w:hop | hop | 0.68 | 0.49 | 182 | 0 | 0.62 | Say, hubby. |
| w:sam | sam | 0.75 | 0.56 | 172 | 299 | 0.59 | Say, Sam. |
| w:it | it | 0.63 | 0.51 | 187 | 0 | 0.22 | Say, |
| w:pam | pam | 0.79 | 0.60 | 183 | 292 | 0.47 | Say, Pamela. |
| w:jet | jet | 0.74 | 0.63 | 186 | 0 | 0.27 | Say, J |
| w:vin | vin | 0.68 | 0.58 | 176 | 202 | 0.67 | Say, Vin. |
| w:a | uh | 0.54 | 0.50 | 168 | 0 | 0.47 | Say, like... |
| w:naps | naps | 0.78 | 0.75 | 179 | 274 | 0.39 | Zay, nabs. |
| w:well | well | 0.76 | 0.51 | 172 | 296 | 0.32 | So, well... |
| w:tan | tan | 0.82 | 0.60 | 181 | 278 | 0.55 | ZAIO TANNO |
| w:bug | bug | 0.77 | 0.65 | 177 | 205 | 0.59 | Say bug it. |
| w:tell | tell | 0.77 | 0.57 | 176 | 288 | 0.85 | So tell me... |
| lt:L1.02:0 | Sam felt nervous walking into the new classroom. E | 6.71 | 7.68 | 172 | 195 | 0.92 | Sam felt nervous walking into the new classroom. E |
| lt:L1.04:0 | Every Tuesday, a truck brings fresh bread to Mr. I | 4.61 | 5.28 | 176 | 197 | 0.93 | Every Tuesday, a truck brings fresh bread to Mr. I |
| read:L1.13:B:1 | Pat has a big box. | 1.51 | 2.07 | 193 | 185 | 0.87 | Pat has a big box. |
| read:L1.13:B:2 | The tag said "b." Dan said, "d?" No, it was "b." I | 4.20 | 7.31 | 181 | 184 | 0.94 | The tag said B. Dan said D. No, it was B. It was a |
| lt:L1.04:2 | Mr. Iqbal called the bakery three times, growing m | 5.11 | 5.79 | 177 | 200 | 0.95 | Mr. Iqbal called the bakery three times, growing m |
| lt:L1.01:1 | Sam's little sister covered her ears and laughed.  | 4.85 | 6.36 | 177 | 222 | 0.95 | Sam's little sister covered her ears and laughed.  |
| q:L1.08:0 | How did the old-fashioned rotation keep people hon | 3.67 | 4.43 | 176 | 209 | 0.95 | How did the old-fashioned rotation keep people hon |
| q:L1.05:1 | How did Bruno seem to feel about the new arrangeme | 4.08 | 5.01 | 177 | 169 | 0.96 | How did Bruno seem to feel about the new arrangeme |