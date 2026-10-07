# Made-up option pronunciation check (tools/check_foils.py)

183 made-up option clips (targets and foils of made-up items), whisper small + small.en, prompt-free decode; a clip passes when either model's heard word has the intended Arpabet (CMUdict lookup, else the course GPC table). Flagged: 52. New characters spent on re-renders: 946 (cap 2000; the second run re-used the first run's renders and spent 11 more).

| foil | rendered as | intended | heard (small / small.en) | action |
|---|---|---|---|---|
| aff | aff | ae f | F / F | no variant heard right; kept original |
| beff | beff | b eh f | Beth / Beth | no variant heard right; kept original |
| bof | bof | b aa f | Bluff. / Bluff. | re-rendered as 'boff' (heard 'Both'/'Bof'), kept |
| cak | kack | k ae k | Cuck. / Cuck. | no variant heard right; kept original |
| cov | cov | k aa v | Cove / Cove | no variant heard right; kept original |
| dakt | dakt | d ae k t | Duct / Ducked | no variant heard right; kept original |
| dut | dut | d ah t | Doot / Do it. | no variant heard right; kept original |
| fekt | fekt | f eh k t | Fact / FACT | re-rendered as 'fehkt' (heard 'Fecht!'/'Fächt'), kept |
| fiff | fiff | f ih f | Fifth. / Fifth | no variant heard right; kept original |
| fom | fom | f aa m | Form / Foam | re-rendered as 'fahm' (heard 'Thumb'/'FOM'), kept |
| fon | fon | f aa n | phone / phone | re-rendered as 'fahn' (heard 'FON'/'Fawn'), kept |
| gep | gep | g eh p | HEP / KEP | re-rendered as 'gepp' (heard 'Yep.'/'GEP'), kept |
| ger | ger | g eh r | gear / get | re-rendered as 'gerr' (heard 'GER'/'GIR'), kept |
| gim | gim | g ih m | GYM / GIMP | re-rendered as 'gihm' (heard 'Gim'/'GIM'), kept |
| gud | gud | g ah d | Good. / Good. | no variant heard right; kept original |
| gug | gug | g ah g | Goog. / Goog. | no variant heard right; kept original |
| guks | guks | g ah k s | Cooks. / Cooks. | no variant heard right; kept original |
| hig | hig | hh ih g | Hague / Hike | re-rendered as 'higg' (heard 'Hig'/'HIG'), kept |
| jov | jov | jh aa v | Jove / Jove | re-rendered as 'jovv' (heard 'Job'/'JOV'), kept |
| lut | lut | l ah t | Lute. / LÜT | re-rendered as 'lutt' (heard 'LUT'/'Lift'), kept |
| meff | meff | m eh f | Meph / Meth | re-rendered as 'mehff' (heard 'myth'/'Meff'), kept |
| moff | moff | m aa f | Moth / Moth | no variant heard right; kept original |
| nam | nam | n ae m | NUM / num | re-rendered as 'namm' (heard 'NEM'/'NAM'), kept |
| nas | nass | n ae s | Ness. / Ness | no variant heard right; kept original |
| nozz | nozz | n aa z | Nause / NAS | no variant heard right; kept original |
| nud | nud | n ah d | Nude / Nude | re-rendered as 'nudd' (heard 'NUD'/'NUD'), kept |
| pag | pag | p ae g | Page. / page | re-rendered as 'pagg' (heard 'Pag.'/'PAG'), kept |
| rop | rop | r aa p | Rope / Rope | no variant heard right; kept original |
| sull | sull | s ah l | Sol / Seoul | no variant heard right; kept original |
| sut | sut | s ah t | Soot / soot | no variant heard right; kept original |
| tem | tem | t eh m | Tim. / 10 | re-rendered as 'temme' (heard 'Temme'/'Temme'), kept |
| tep | tep | t eh p | Tip / Tip. | re-rendered as 'tepp' (heard 'Tip'/'TEP'), kept |
| tiss | tiss | t ih s | Cheers! / Tis. | re-rendered as 'tihss' (heard 'Tiss'/'Tis'), kept |
| tud | tud | t ah d | Tood. / Tude | re-rendered as 'tudd' (heard 'Tud.'/'TUD'), kept |
| tum | tum | t ah m | Tomb / Toon | re-rendered as 'tuhm' (heard 'TUM'/'TUM'), kept |
| tup | tup | t ah p | Top. / Top | no variant heard right; kept original |
| uff | uff | ah f | Oof. / Oof. | no variant heard right; kept original |
| ust | ust | ah s t | Boost / Boost | re-rendered as 'uhst' (heard 'Ust'/'Ust'), kept |
| vab | vab | v ae b | VUB / verb | re-rendered as 'vabbe' (heard 'Wabbe!'/'VAB'), kept |
| vav | vav | v ae v | Vove / VOV | no variant heard right; kept original |
| vib | vib | v ih b | Vibe / Vibe | re-rendered as 'vibb' (heard 'Vib'/'Vib'), kept |
| vum | vum | v ah m | VOOM / Voom | no variant heard right; kept original |
| wav | wav | w ae v | Wave. / wave | re-rendered as 'wahv' (heard 'WEV'/'WAV'), kept |
| wov | wov | w aa v | wove / WOVE | no variant heard right; kept original |
| wuff | wuff | w ah f | Woof! / Woof! | no variant heard right; kept original |
| wuk | wuk | w ah k | Work. / Wook | no variant heard right; kept original |
| wux | wux | w ah k s | Woosh. / Whoosh! | no variant heard right; kept original |
| yit | yit | y ih t | Yet / Yet. | no variant heard right; kept original |
| zer | zer | z eh r | There. / There | re-rendered as 'zehr' (heard 'ZEHR'/'There.'), kept |
| ziss | ziss | z ih s | This. / This. | no variant heard right; kept original |
| zuks | zuks | z ah k s | Zooks / Zooks | re-rendered as 'zuhks' (heard 'Zucks.'/'Zucks.'), kept |
| zur | zur | z ah r | Sua / Sua | no variant heard right; kept original |
