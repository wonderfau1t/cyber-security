from eax_cfb.cfb import CFBCipher
from eax_cfb.eax import EAXCFB
from eax_cfb.kdf import kdf
from eax_cfb.message_padder import MessagePadder
from eax_cfb.packet_handler import PacketHandler
from core.produce_round_keys import produce_round_keys
from core.utils import msg2bin

print("Тест KDF")
pass1 = "ЧЕЧЕТКА"
salt1 = "СЕАНС"
context = ["СЕАНСОВЫЙ_КЛЮЧ", "КЛЮЧ_РАСПРЕДЕЛЕНИЯ_КЛЮЧЕЙ"]
size = [32, 16]
print(kdf(pass1, salt1, context, size, 2))
print("============")

inputs_array = [
    "ГАРРИ_С_ОТКРЫТЫМ_РТОМ_СМОТРЕЛ_НА_СЕМЕЙНОЕ_ХРАНИЛИЩЕ_ТЧК_У_НЕГО_БЫЛО_ТАК_МНОГО_ВОПРОСОВ_ЗПТ_ЧТО_ОН_ДАЖЕ_НЕ_ЗНАЛ_ЗПТ_С_КАКОГО_ИМЕННО_НАЧАТЬ_ТЧК_МАКГОНАГАЛЛ_СТОЯЛА_У_ДВЕРИ_И_НАБЛЮДАЛА_ЗА_МАЛЬЧИКОМ_ТЧК_ОНА_НЕБРЕЖНО_ОПИРАЛАСЬ_О_СТЕНУ_ЗПТ_НО_ВЗГЛЯД_У_НЕЕ_БЫЛ_НАПРЯЖЕННЫЙ_ТЧК_И_НЕСПРОСТА_ТЧК_ОКАЗАТЬСЯ_ПЕРЕД_ОГРОМНОЙ_КУЧЕЙ_ЗОЛОТЫХ_МОНЕТ_ТИРЕ_ТА_ЕЩЕ_ПРОВЕРКА_НА_ПРОЧНОСТЬ_ТЧК_",
    "ИСТОРИЯ_ГАНСА_КАСТОРПА_ЗПТ_КОТОРУЮ_МЫ_ХОТИМ_ЗДЕСЬ_РАССКАЗАТЬ_ЗПТ_ТИРЕ_ОТНЮДЬ_НЕ_РАДИ_НЕГО_ПОСКОЛЬКУ_ЧИТАТЕЛЬ_В_ЕГО_ЛИЦЕ_ПОЗНАКОМИТСЯ_ЛИШЬ_С_САМЫМ_ОБЫКНОВЕННЫМ_ЗПТ_ХОТЯ_И_ПРИЯТНЫМ_МОЛОДЫМ_ЧЕЛОВЕКОМ_ЗПТ_ТИРЕ_ИЗЛАГАЕТСЯ_РАДИ_САМОЙ_ЭТОЙ_ИСТОРИИ_ЗПТ_ИБО_ОНА_КАЖЕТСЯ_НАМ_В_ВЫСОКОЙ_СТЕПЕНИ_ДОСТОЙНОЙ_ОПИСАНИЯ_ПРИЧЕМ_ЗПТ_К_ЧЕСТИ_ГАНСА_КАСТОРПА_ЗПТ_СЛЕДУЕТ_ОТМЕТИТЬ_ЗПТ_ЧТО_ЭТО_ИМЕННО_ЕГО_ИСТОРИЯ_ЗПТ_А_ВЕДЬ_НЕ_С_ЛЮБЫМ_И_КАЖДЫМ_ЧЕЛОВЕКОМ_МОЖЕТ_СЛУЧИТЬСЯ_ИСТОРИЯ_ТЧК_ТАК_ВОТ_ДВТЧ_ЭТА_ИСТОРИЯ_ПРОИЗОШЛА_МНОГО_ВРЕМЕНИ_НАЗАД_ЗПТ_ОНА_ЗПТ_ТАК_СКАЗАТЬ_ЗПТ_УЖЕ_ПОКРЫЛАСЬ_БЛАГОРОДНОЙ_РЖАВЧИНОЙ_СТАРИНЫ_ЗПТ_И_ПОВЕСТВОВАНИЕ_О_НЕЙ_ДОЛЖНО_ЗПТ_РАЗУМЕЕТСЯ_ЗПТ_ВЕСТИСЬ_В_ФОРМАХ_ДАВНО_ПРОШЕДШЕГО_ТЧК_ДЛЯ_ИСТОРИИ_ЭТО_НЕ_ТАКОЙ_УЖ_БОЛЬШОЙ_НЕДОСТАТОК_ЗПТ_СКОРЕЕ_ДАЖЕ_ПРЕИМУЩЕСТВО_ЗПТ_ИБО_ЛЮБАЯ_ИСТОРИЯ_ДОЛЖНА_БЫТЬ_ПРОШЛЫМ_ЗПТ_И_ЧЕМ_БОЛЕЕ_ОНА_ТИРЕ_ПРОШЛОЕ_ЗПТ_ТЕМ_ЛУЧШЕ_И_ДЛЯ_ЕЕ_ОСОБЕННОСТЕЙ_КАК_ИСТОРИИ_И_ДЛЯ_РАССКАЗЧИКА_ЗПТ_КОТОРЫЙ_БОРМОЧЕТ_СВОИ_ЗАКЛИНАНИЯ_НАД_ПРОШЕДШИМИ_ВРЕМЕНАМИ_ТЧК_ОДНАКО_ПРИХОДИТСЯ_ПРИЗНАТЬ_ЗПТ_ЧТО_ОНА_ЗПТ_ТАК_ЖЕ_КАК_В_НАШУ_ЭПОХУ_И_САМИ_ЛЮДИ_ЗПТ_ОСОБЕННО_ЖЕ_РАССКАЗЧИКИ_ИСТОРИЙ_ЗПТ_ГОРАЗДО_СТАРЕЕ_СВОИХ_ЛЕТ_ЗПТ_ЕЕ_ВОЗРАСТ_ИЗМЕРЯЕТСЯ_НЕ_ПРОТЕКШИМИ_ДНЯМИ_ЗПТ_И_БРЕМЯ_ЕЕ_ГОДОВ_ТИРЕ_НЕ_ЧИСЛОМ_ОБРАЩЕНИЙ_ЗЕМЛИ_ВОКРУГ_СОЛНЦА_ТЧК_СЛОВОМ_ЗПТ_ОНА_ОБЯЗАНА_СТЕПЕНЬЮ_СВОЕЙ_ДАВНОСТИ_НЕ_САМОМУ_ВРЕМЕНИ_ТЧК_ОТМЕТИМ_ЗПТ_ЧТО_В_ЭТИХ_СЛОВАХ_МЫ_ДАЕМ_МИМОХОДОМ_НАМЕК_И_УКАЗАНИЕ_НА_СОМНИТЕЛЬНОСТЬ_И_СВОЕОБРАЗНУЮ_ДВОЙСТВЕННОСТЬ_ТОЙ_ЗАГАДОЧНОЙ_СТИХИИ_ЗПТ_КОТОРАЯ_ЗОВЕТСЯ_ВРЕМЕНЕМ_ТЧК_ОДНАКО_ЗПТ_НЕ_ЖЕЛАЯ_ИСКУССТВЕННО_ЗАТЕМНЯТЬ_ВОПРОС_ЗПТ_ПО_СУЩЕСТВУ_СОВЕРШЕННО_ЯСНЫЙ_ЗПТ_СКАЖЕМ_СЛЕДУЮЩЕЕ_ДВТЧ_ОСОБАЯ_ДАВНОСТЬ_НАШЕЙ_ИСТОРИИ_ЗАВИСИТ_ЕЩЕ_И_ОТ_ТОГО_ЗПТ_ЧТО_ОНА_ПРОИСХОДИТ_НА_НЕКОЕМ_РУБЕЖЕ_И_ПЕРЕД_ПОВОРОТОМ_ЗПТ_ГЛУБОКО_РАСЩЕПИВШИМ_НАШУ_ЖИЗНЬ_И_СОЗНАНИЕ_МНГТЧ_ОНА_ПРОИСХОДИТ_ЗПТ_ИЛИ_ЗПТ_ЧТОБЫ_ИЗБЕЖАТЬ_ВСЯКИХ_ФОРМ_НАСТОЯЩЕГО_ЗПТ_СКАЖЕМ_ЗПТ_ПРОИСХОДИЛА_ЗПТ_ПРОИЗОШЛА_НЕКОГДА_ЗПТ_КОГДА_ТИРЕ_ТО_ЗПТ_В_СТАРОДАВНИЕ_ВРЕМЕНА_ЗПТ_В_ДНИ_ПЕРЕД_ВЕЛИКОЙ_ВОЙНОЙ_ЗПТ_С_НАЧАЛОМ_КОТОРОЙ_НАЧАЛОСЬ_СТОЛЬ_МНОГОЕ_ЗПТ_ЧТО_ПОТОМ_ОНО_УЖЕ_И_НЕ_ПЕРЕСТАВАЛО_НАЧИНАТЬСЯ_ТЧК_ИТАК_ЗПТ_ОНА_ПРОИСХОДИТ_ПЕРЕД_ТЕМ_ПОВОРОТОМ_ЗПТ_ПРАВДА_НЕЗАДОЛГО_ДО_НЕГО_ТЧК_НО_РАЗВЕ_ХАРАКТЕР_ДАВНОСТИ_КАКОЙ_ТИРЕ_НИБУДЬ_ИСТОРИИ_НЕ_СТАНОВИТСЯ_ТЕМ_ГЛУБЖЕ_ЗПТ_СОВЕРШЕННЕЕ_И_СКАЗОЧНЕЕ_ЗПТ_ЧЕМ_БЛИЖЕ_ОНА_К_ЭТОМУ_ПЕРЕД_ТЕМ_ВПРС_КРОМЕ_ТОГО_ЗПТ_НАША_ИСТОРИЯ_ЗПТ_БЫТЬ_МОЖЕТ_ЗПТ_И_ПО_СВОЕЙ_ВНУТРЕННЕЙ_ПРИРОДЕ_НЕ_ЛИШЕНА_НЕКОТОРОЙ_СВЯЗИ_СО_СКАЗКОЙ_ТЧК_МЫ_БУДЕМ_ОПИСЫВАТЬ_ЕЕ_ВО_ВСЕХ_ПОДРОБНОСТЯХ_ЗПТ_ТОЧНО_И_ОБСТОЯТЕЛЬНО_ЗПТ_ТИРЕ_ИБО_КОГДА_ЖЕ_ВРЕМЯ_ПРИ_ИЗЛОЖЕНИИ_КАКОЙ_ТИРЕ_НИБУДЬ_ИСТОРИИ_ЛЕТЕЛО_ИЛИ_ТЯНУЛОСЬ_ПО_ПОДСКАЗКЕ_ПРОСТРАНСТВА_И_ВРЕМЕНИ_ЗПТ_КОТОРЫЕ_НУЖНЫ_ДЛЯ_ЕЕ_РАЗВЕРТЫВАНИЯ_ВПРС_НЕ_ОПАСАЯСЬ_УПРЕКА_В_ПЕДАНТИЗМЕ_ЗПТ_МЫ_СКОРЕЕ_СКЛОННЫ_УТВЕРЖДАТЬ_ЗПТ_ЧТО_ЛИШЬ_ОСНОВАТЕЛЬНОСТЬ_МОЖЕТ_БЫТЬ_ЗАНИМАТЕЛЬНОЙ_ТЧК_СЛЕДОВАТЕЛЬНО_ЗПТ_ОДНИМ_МАХОМ_РАССКАЗЧИК_С_ИСТОРИЕЙ_ГАНСА_НЕ_СПРАВИТСЯ_ТЧК_СЕМИ_ДНЕЙ_НЕДЕЛИ_НА_НЕЕ_НЕ_ХВАТИТ_ЗПТ_НЕ_ХВАТИТ_И_СЕМИ_МЕСЯЦЕВ_ТЧК_САМОЕ_ЛУЧШЕЕ_ТИРЕ_И_НЕ_СТАРАТЬСЯ_УЯСНИТЬ_СЕБЕ_ЗАРАНЕЕ_ЗПТ_СКОЛЬКО_ИМЕННО_ПРОЙДЕТ_ЗЕМНОГО_ВРЕМЕНИ_ЗПТ_ПОКА_ОНА_БУДЕТ_ДЕРЖАТЬ_ЕГО_В_СВОИХ_ТЕНЕТАХ_ТЧК_СЕМИ_ЛЕТ_ЗПТ_ДАСТ_БОГ_ЗПТ_ВСЕ_ЖЕ_НЕ_ПОНАДОБИТСЯ_ТЧК_ИТАК_ЗПТ_МЫ_НАЧИНАЕМ_ТЧК",
    "ЛОРДЫ_И_ЛЕДИ_ВИЗЕНГАМОТА_В_ФИОЛЕТОВЫХ_МАНТИЯХ_ЗПТ_ОТМЕЧЕННЫХ_СЕРЕБРЯНОЙ_ЛИТЕРОЙ_В_ЗПТ_С_ХОЛОДНЫМ_УПРЕКОМ_СМОТРЕЛИ_НА_ДРОЖАЩУЮ_ДЕВОЧКУ_ЗПТ_ЗАКОВАННУЮ_В_ЦЕПИ_ТЧК_ЕСЛИ_В_РАМКАХ_КАКОЙТО_ЭТИЧЕСКОЙ_СИСТЕМЫ_ОНИ_И_ПОРИЦАЛИ_СЕБЯ_ЗПТ_ТО_ОПРЕДЕЛЕННО_СТАВИЛИ_ЭТО_СЕБЕ_В_ЗАСЛУГУ_ТЧК_ГАРРИ_С_ТРУДОМ_МОГ_РОВНО_ДЫШАТЬ_ТЧК_ЕГО_ТЕМНАЯ_СТОРОНА_ПРИДУМАЛА_ПЛАН_МНГТЧ_И_ОТСТУПИЛА_НАЗАД_ТЧК_СЛИШКОМ_ЛЕДЯНОЙ_ТОН_НЕ_ПОЙДЕТ_НА_ПОЛЬЗУ_ГЕРМИОНЕ_ТЧК_БУДУЧИ_ЛИШЬ_НАПОЛОВИНУ_ПОГРУЖЕННЫМ_В_СВОЮ_ТЕМНУЮ_СТОРОНУ_ЗПТ_ГАРРИ_ПОЧЕМУТО_ЭТОГО_НЕ_ПОНИМАЛ_МНГТЧ",
    "А_БЖ0101011010111101011010101010101001111010100101011010101010100101001010010101010001010101001010101011101100111111011101",
    "ОБЖ_ГОД_В_Я011",
    "ШИФРОПАНКИ_ЭТО_НЕФОРМАЛЬНАЯ_ГРУППА_ЛЮДЕЙ_ЗПТ_ЗАИНТЕРЕСОВАННЫХ_В_СОХРАНЕНИИ_АНОНИМНОСТИ_И_ИНТЕРЕСУЮЩИХСЯ_КРИПТОГРАФИЕЙ_ТЧК_ПЕРВОНАЧАЛЬНО_ШИФРОПАНКИ_ОБЩАЛИСЬ_С_ПОМОЩЬЮ_СЕТИ_АНОНИМНЫХ_РЕМЕЙЛЕРОВ_ТЧК_ЦЕЛЬЮ_ДАННОЙ_ГРУППЫ_БЫЛО_ДОСТИЖЕНИЕ_АНОНИМНОСТИ_И_БЕЗОПАСНОСТИ_ПОСРЕДСТВОМ_АКТИВНОГО_ИСПОЛЬЗОВАНИЯ_КРИПТОГРАФИИ_ТЧК",
]

assocdata_array = [
    ["ВА", "АЛИСА_А", "БОБ___А", "КОТОПОЕЗД"],
    ["ВБ", "АЛИСА_АЖ", "БОБ___ОЧ", "ЕГИПТЯНИН"],
    ["В_", "АЛИСА_ЯЗ", "БОБ___ЬЬ", "ЩЕГОЛЯНИЕ"],
    ["ВБ", "БОБ___ЬЬ", "АЛИСА_ЯЗ", "ЭКЛАМПСИЯ"],
    ["ВБ", "БОБ___ЬЬ", "АЛИСА_ЯЗ", "ЕГИПТЯНИН"],
    ["ВБ", "АЛИСА_ЯЗ", "БОБ___ЬЬ", "ЕГИПТЯНИН"],
]

print("Тест конвертера")
l_L = len(inputs_array)
print(l_L)
for i in range(l_L):
    print(len(msg2bin(inputs_array[i])))
print("============")

print("Тест паддера")
padder = MessagePadder()
in_ = inputs_array[0]
inter = padder.pad_message(in_)
print(len(msg2bin(inter)))
out = padder.unpad_message(inter)
print(len(msg2bin(out)))

print("+++++++++")
in_ = inputs_array[1]
tmp = MessagePadder()._check_padding(msg2bin(in_))
print(tmp)
inter = padder.pad_message(in_)
print(len(msg2bin(inter)))
tmp = MessagePadder()._check_padding(msg2bin(inter))
print(tmp)
out = padder.unpad_message(inter)
print(len(msg2bin(out)))
print(out == in_)

print("+++++++++")
in1 = inputs_array[2]
in2 = padder.pad_message(in1)
tmp = MessagePadder()._check_padding(msg2bin(in2))
print(tmp)
inter = padder.pad_message(in2)
print(len(msg2bin(inter)))
tmp = MessagePadder()._check_padding(msg2bin(inter))
print(tmp)
out = padder.unpad_message(inter)
print(len(msg2bin(out)))
print(out == in2)

print("+++++++++")
in_ = inputs_array[3]
inter = padder.pad_message(in_)
print(len(msg2bin(inter)))
tmp = MessagePadder()._check_padding(msg2bin(inter))
print(tmp)
out = padder.unpad_message(inter)
print(len(msg2bin(out)))
print(msg2bin(out) == msg2bin(in_))
print("============")

print("Тест передачи пакетов")
packet = PacketHandler()
xtst = packet.prepare_packet(assocdata_array[1], "КОЛЕСО", inputs_array[1])
ytst = packet.receive(packet.transmit(xtst))
print(xtst[0], xtst[1], xtst[3])
print(xtst[2] == ytst[2])
q = packet.transmit(xtst)
print(ytst[0], ytst[1], ytst[3])
print(ytst[2][:100] + "...")
print(packet.validate_packet(ytst))
print("============")

print("Тест textxor")
a1 = "ГОЛОВКА_КРУЖИТСЯ"
a2 = "МЫШКА_БЫЛА_ЛИХОЙ"
b1 = "СИНЕВАТАЯ_БОРОДА"
b2 = "ЗЕЛЕНЫЙ_КОТОЗМИЙ"
cipher = CFBCipher()
c1 = cipher._textxor(a1, a2)
c2 = cipher._textxor(a1, b2)
print(c1, c2)
c11 = cipher._textxor(c1, a2)
c12 = cipher._textxor(c1, a1)
print(c11, c12)
c21 = cipher._textxor(c2, a1)
c22 = cipher._textxor(c2, a2)
print(c21, c22)
print("============")

print("Тест CFB")
tst = inputs_array[0]
iv1 = "АЛИСА_УМЕЕТ_ПЕТЬ"
iv2 = "БОБ_НЕМНОГО_ПЬЯН"
keyset = produce_round_keys("СЕАНСОВЫЙ_КЛЮЧИК", 8)
print(tst[:100] + "...")
print(keyset)
cfb = CFBCipher()

print("CFB Frw")
f_test1m = cfb.frw_cfb(tst, iv1, keyset, 1)
print(f_test1m[:100] + "...")
print(len(f_test1m), f_test1m[368 : 368 + 16])

print("CFB Inv")
i_test1m = cfb.inv_cfb(f_test1m, iv1, keyset, 1)
print(i_test1m[:100] + "...")
print(i_test1m[368 : 368 + 16])

print("CFB Frw")
f_test1 = cfb.frw_cfb(tst, iv1, keyset, 0)
print(len(f_test1), f_test1[368 : 368 + 16])

print("Проверка")
i_test10 = cfb.inv_cfb(f_test1, iv1, keyset, 1)
i_test1 = cfb.inv_cfb(f_test1, iv1, keyset, 0)
print(i_test10 == tst)
print(i_test1 == tst)

print("CFB Frw")
f_test2 = cfb.frw_cfb(tst, iv2, keyset, 1)
i_test2 = cfb.inv_cfb(f_test2, iv2, keyset, 1)
print(i_test2[:100] + "...")
i_test21 = cfb.inv_cfb(f_test2, iv1, keyset, 1)
print(i_test21[:100] + "...")
print(i_test2[368 : 368 + 16], i_test21[368 : 368 + 16])

print("ТЕСТ EAXCFB")
ad = assocdata_array[1]
ad[4] = "АБВГД"
packet = [ad, "БОБ_НЕМНОГО_ПЬЯН", inputs_array[0], ""]
print(ad)
cad_in = "ПОКА_ЕЩЕ_НЕВАЖНО"
sec_in = "ТОЖЕ_ЕЩЕ_НЕВАЖНО"
cad = ad[0] + ad[1] + ad[2] + ad[3] + "_____"
cadmac = cfb.frw_cfb(cad, sec_in, keyset, -1)
eax = EAXCFB()

print("Тест 1")
q_test1m = eax.eax_cfb_frw(packet, cadmac, keyset, sec_in, 0)
print(q_test1m[3], q_test1m[2][:100] + "...")
r_test1m = eax.eax_cfb_inv(q_test1m, keyset, sec_in, 0)
print(r_test1m[3], r_test1m[2][:100] + "...")
print("+" * 16)

print("Тест 2")
q_test0m = eax.eax_cfb_frw(packet, cadmac, keyset, sec_in, 1)
print(q_test0m[3], q_test0m[2][:100] + "...")
r_test0m = eax.eax_cfb_inv(q_test0m, keyset, sec_in, 1)
print(r_test0m[3], r_test0m[2][:100] + "...")
print("+" * 16)

print("========")
ad = assocdata_array[3]
messages = inputs_array
channel = eax.eax_cfb(ad, messages, "СЕАНСОВЫЙ_КЛЮЧИК", "СЕМИХАТОВ_КВАНТЫ", "send")
for i in channel:
    print(len(i))


def invert(stream_in, n_in):
    q = stream_in[n_in]
    stream_in[n_in] = (q + 1) % 2
    return stream_in


channel[0] = invert(channel[0], 317)
channel[3] = invert(channel[3], 12)
transmission = eax.eax_cfb(ad, channel, "СЕАНСОВЫЙ_КЛЮЧИК", "СЕМИХАТОВ_КВАНТЫ", "receive")
for i in transmission:
    print(i[0])
for i in transmission:
    print(i[1])
for i in transmission:
    print(i[2][:100] + "...")

print(
    transmission[0][2] == messages[0],
    transmission[1][2] == messages[1],
    transmission[2][2] == messages[2],
    transmission[3][2] == messages[3],
    transmission[4][2] == messages[4],
    transmission[5][2] == messages[5],
)
print(msg2bin(transmission[3][2]) == msg2bin(messages[3]))
for i in transmission:
    print(i[3])
