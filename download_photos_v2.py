"""
BAZUMI — повторное скачивание фото (устойчивая версия)
Уже скачанные пропускает. Делает по 3 попытки на каждый файл с разными таймаутами.
Запускать в той же папке где index.html и папка photos/.

Использование:
    python download_photos_v2.py
"""
import os, sys, time
import urllib.request
import urllib.error
import socket

PHOTOS = [
    ('784073384', 'https://basket-36.wbbasket.ru/vol7840/part784073/784073384/images/big/1.webp'),
    ('784070994', 'https://basket-36.wbbasket.ru/vol7840/part784070/784070994/images/big/1.webp'),
    ('785885994', 'https://basket-36.wbbasket.ru/vol7858/part785885/785885994/images/big/1.webp'),
    ('788522562', 'https://basket-36.wbbasket.ru/vol7885/part788522/788522562/images/big/1.webp'),
    ('788538793', 'https://basket-36.wbbasket.ru/vol7885/part788538/788538793/images/big/1.webp'),
    ('788538794', 'https://basket-36.wbbasket.ru/vol7885/part788538/788538794/images/big/1.webp'),
    ('411186575', 'https://basket-23.wbbasket.ru/vol4111/part411186/411186575/images/big/1.webp'),
    ('697259046', 'https://basket-33.wbbasket.ru/vol6972/part697259/697259046/images/big/1.webp'),
    ('814554535', 'https://basket-37.wbbasket.ru/vol8145/part814554/814554535/images/big/1.webp'),
    ('890330650', 'https://basket-39.wbbasket.ru/vol8903/part890330/890330650/images/big/1.webp'),
    ('890344840', 'https://basket-39.wbbasket.ru/vol8903/part890344/890344840/images/big/1.webp'),
    ('411199026', 'https://basket-23.wbbasket.ru/vol4111/part411199/411199026/images/big/1.webp'),
    ('496421739', 'https://basket-27.wbbasket.ru/vol4964/part496421/496421739/images/big/1.webp'),
    ('526212185', 'https://basket-28.wbbasket.ru/vol5262/part526212/526212185/images/big/1.webp'),
    ('334593676', 'https://basket-20.wbbasket.ru/vol3345/part334593/334593676/images/big/1.webp'),
    ('411180653', 'https://basket-23.wbbasket.ru/vol4111/part411180/411180653/images/big/1.webp'),
    ('207077279', 'https://basket-14.wbbasket.ru/vol2070/part207077/207077279/images/big/1.webp'),
    ('207081334', 'https://basket-14.wbbasket.ru/vol2070/part207081/207081334/images/big/1.webp'),
    ('207081335', 'https://basket-14.wbbasket.ru/vol2070/part207081/207081335/images/big/1.webp'),
    ('160485380', 'https://basket-11.wbbasket.ru/vol1604/part160485/160485380/images/big/1.webp'),
    ('160482833', 'https://basket-11.wbbasket.ru/vol1604/part160482/160482833/images/big/1.webp'),
    ('160483951', 'https://basket-11.wbbasket.ru/vol1604/part160483/160483951/images/big/1.webp'),
    ('366637479', 'https://basket-21.wbbasket.ru/vol3666/part366637/366637479/images/big/1.webp'),
    ('371972747', 'https://basket-22.wbbasket.ru/vol3719/part371972/371972747/images/big/1.webp'),
    ('489544548', 'https://basket-27.wbbasket.ru/vol4895/part489544/489544548/images/big/1.webp'),
    ('150611004', 'https://basket-10.wbbasket.ru/vol1506/part150611/150611004/images/big/1.webp'),
    ('160989316', 'https://basket-11.wbbasket.ru/vol1609/part160989/160989316/images/big/1.webp'),
    ('160989317', 'https://basket-11.wbbasket.ru/vol1609/part160989/160989317/images/big/1.webp'),
    ('207076751', 'https://basket-14.wbbasket.ru/vol2070/part207076/207076751/images/big/1.webp'),
    ('16471974', 'https://basket-02.wbbasket.ru/vol164/part16471/16471974/images/big/1.webp'),
    ('16996621', 'https://basket-02.wbbasket.ru/vol169/part16996/16996621/images/big/1.webp'),
    ('415775006', 'https://basket-24.wbbasket.ru/vol4157/part415775/415775006/images/big/1.webp'),
    ('415775009', 'https://basket-24.wbbasket.ru/vol4157/part415775/415775009/images/big/1.webp'),
    ('415775010', 'https://basket-24.wbbasket.ru/vol4157/part415775/415775010/images/big/1.webp'),
    ('499510299', 'https://basket-27.wbbasket.ru/vol4995/part499510/499510299/images/big/1.webp'),
    ('499510558', 'https://basket-27.wbbasket.ru/vol4995/part499510/499510558/images/big/1.webp'),
    ('499512074', 'https://basket-27.wbbasket.ru/vol4995/part499512/499512074/images/big/1.webp'),
    ('758113090', 'https://basket-35.wbbasket.ru/vol7581/part758113/758113090/images/big/1.webp'),
    ('758113091', 'https://basket-35.wbbasket.ru/vol7581/part758113/758113091/images/big/1.webp'),
    ('758113092', 'https://basket-35.wbbasket.ru/vol7581/part758113/758113092/images/big/1.webp'),
    ('16062287', 'https://basket-02.wbbasket.ru/vol160/part16062/16062287/images/big/1.webp'),
    ('70297358', 'https://basket-04.wbbasket.ru/vol702/part70297/70297358/images/big/1.webp'),
    ('70297359', 'https://basket-04.wbbasket.ru/vol702/part70297/70297359/images/big/1.webp'),
    ('16471971', 'https://basket-02.wbbasket.ru/vol164/part16471/16471971/images/big/1.webp'),
    ('16753662', 'https://basket-02.wbbasket.ru/vol167/part16753/16753662/images/big/1.webp'),
    ('783983461', 'https://basket-36.wbbasket.ru/vol7839/part783983/783983461/images/big/1.webp'),
    ('783983462', 'https://basket-36.wbbasket.ru/vol7839/part783983/783983462/images/big/1.webp'),
    ('371976559', 'https://basket-22.wbbasket.ru/vol3719/part371976/371976559/images/big/1.webp'),
    ('712214311', 'https://basket-34.wbbasket.ru/vol7122/part712214/712214311/images/big/1.webp'),
    ('712214312', 'https://basket-34.wbbasket.ru/vol7122/part712214/712214312/images/big/1.webp'),
    ('712214313', 'https://basket-34.wbbasket.ru/vol7122/part712214/712214313/images/big/1.webp'),
    ('371989529', 'https://basket-22.wbbasket.ru/vol3719/part371989/371989529/images/big/1.webp'),
    ('371989531', 'https://basket-22.wbbasket.ru/vol3719/part371989/371989531/images/big/1.webp'),
    ('371989534', 'https://basket-22.wbbasket.ru/vol3719/part371989/371989534/images/big/1.webp'),
    ('499509762', 'https://basket-27.wbbasket.ru/vol4995/part499509/499509762/images/big/1.webp'),
    ('534373656', 'https://basket-28.wbbasket.ru/vol5343/part534373/534373656/images/big/1.webp'),
    ('695404626', 'https://basket-33.wbbasket.ru/vol6954/part695404/695404626/images/big/1.webp'),
    ('697255106', 'https://basket-33.wbbasket.ru/vol6972/part697255/697255106/images/big/1.webp'),
    ('712201638', 'https://basket-34.wbbasket.ru/vol7122/part712201/712201638/images/big/1.webp'),
    ('371975475', 'https://basket-22.wbbasket.ru/vol3719/part371975/371975475/images/big/1.webp'),
    ('371977217', 'https://basket-22.wbbasket.ru/vol3719/part371977/371977217/images/big/1.webp'),
    ('207083047', 'https://basket-14.wbbasket.ru/vol2070/part207083/207083047/images/big/1.webp'),
    ('156205418', 'https://basket-10.wbbasket.ru/vol1562/part156205/156205418/images/big/1.webp'),
    ('140129555', 'https://basket-10.wbbasket.ru/vol1401/part140129/140129555/images/big/1.webp'),
    ('150603071', 'https://basket-10.wbbasket.ru/vol1506/part150603/150603071/images/big/1.webp'),
    ('155202025', 'https://basket-10.wbbasket.ru/vol1552/part155202/155202025/images/big/1.webp'),
    ('415722041', 'https://basket-24.wbbasket.ru/vol4157/part415722/415722041/images/big/1.webp'),
    ('415722042', 'https://basket-24.wbbasket.ru/vol4157/part415722/415722042/images/big/1.webp'),
    ('173127865', 'https://basket-12.wbbasket.ru/vol1731/part173127/173127865/images/big/1.webp'),
    ('173129768', 'https://basket-12.wbbasket.ru/vol1731/part173129/173129768/images/big/1.webp'),
    ('240144769', 'https://basket-15.wbbasket.ru/vol2401/part240144/240144769/images/big/1.webp'),
    ('221724457', 'https://basket-15.wbbasket.ru/vol2217/part221724/221724457/images/big/1.webp'),
    ('207083544', 'https://basket-14.wbbasket.ru/vol2070/part207083/207083544/images/big/1.webp'),
    ('58280757', 'https://basket-04.wbbasket.ru/vol582/part58280/58280757/images/big/1.webp'),
    ('58282409', 'https://basket-04.wbbasket.ru/vol582/part58282/58282409/images/big/1.webp'),
    ('66896745', 'https://basket-04.wbbasket.ru/vol668/part66896/66896745/images/big/1.webp'),
    ('411184264', 'https://basket-23.wbbasket.ru/vol4111/part411184/411184264/images/big/1.webp'),
    ('411184265', 'https://basket-23.wbbasket.ru/vol4111/part411184/411184265/images/big/1.webp'),
    ('411184268', 'https://basket-23.wbbasket.ru/vol4111/part411184/411184268/images/big/1.webp'),
    ('411176831', 'https://basket-23.wbbasket.ru/vol4111/part411176/411176831/images/big/1.webp'),
    ('411177778', 'https://basket-23.wbbasket.ru/vol4111/part411177/411177778/images/big/1.webp'),
    ('785850522', 'https://basket-36.wbbasket.ru/vol7858/part785850/785850522/images/big/1.webp'),
    ('785874431', 'https://basket-36.wbbasket.ru/vol7858/part785874/785874431/images/big/1.webp'),
    ('784072367', 'https://basket-36.wbbasket.ru/vol7840/part784072/784072367/images/big/1.webp'),
    ('758185521', 'https://basket-35.wbbasket.ru/vol7581/part758185/758185521/images/big/1.webp'),
    ('721182263', 'https://basket-34.wbbasket.ru/vol7211/part721182/721182263/images/big/1.webp'),
    ('721182264', 'https://basket-34.wbbasket.ru/vol7211/part721182/721182264/images/big/1.webp'),
    ('677118970', 'https://basket-33.wbbasket.ru/vol6771/part677118/677118970/images/big/1.webp'),
    ('712216156', 'https://basket-34.wbbasket.ru/vol7122/part712216/712216156/images/big/1.webp'),
    ('371982284', 'https://basket-22.wbbasket.ru/vol3719/part371982/371982284/images/big/1.webp'),
    ('81335880', 'https://basket-05.wbbasket.ru/vol813/part81335/81335880/images/big/1.webp'),
    ('150606046', 'https://basket-10.wbbasket.ru/vol1506/part150606/150606046/images/big/1.webp'),
    ('202827020', 'https://basket-13.wbbasket.ru/vol2028/part202827/202827020/images/big/1.webp'),
    ('200773929', 'https://basket-13.wbbasket.ru/vol2007/part200773/200773929/images/big/1.webp'),
    ('200775006', 'https://basket-13.wbbasket.ru/vol2007/part200775/200775006/images/big/1.webp'),
    ('200775812', 'https://basket-13.wbbasket.ru/vol2007/part200775/200775812/images/big/1.webp'),
    ('526216833', 'https://basket-28.wbbasket.ru/vol5262/part526216/526216833/images/big/1.webp'),
    ('783977688', 'https://basket-36.wbbasket.ru/vol7839/part783977/783977688/images/big/1.webp'),
    ('783977689', 'https://basket-36.wbbasket.ru/vol7839/part783977/783977689/images/big/1.webp'),
    ('160493280', 'https://basket-11.wbbasket.ru/vol1604/part160493/160493280/images/big/1.webp'),
    ('216982636', 'https://basket-14.wbbasket.ru/vol2169/part216982/216982636/images/big/1.webp'),
    ('237506535', 'https://basket-15.wbbasket.ru/vol2375/part237506/237506535/images/big/1.webp'),
    ('239904692', 'https://basket-15.wbbasket.ru/vol2399/part239904/239904692/images/big/1.webp'),
    ('239905190', 'https://basket-15.wbbasket.ru/vol2399/part239905/239905190/images/big/1.webp'),
    ('310898888', 'https://basket-19.wbbasket.ru/vol3108/part310898/310898888/images/big/1.webp'),
    ('366634451', 'https://basket-21.wbbasket.ru/vol3666/part366634/366634451/images/big/1.webp'),
    ('756161528', 'https://basket-35.wbbasket.ru/vol7561/part756161/756161528/images/big/1.webp'),
    ('756161529', 'https://basket-35.wbbasket.ru/vol7561/part756161/756161529/images/big/1.webp'),
    ('784082522', 'https://basket-36.wbbasket.ru/vol7840/part784082/784082522/images/big/1.webp'),
    ('784082523', 'https://basket-36.wbbasket.ru/vol7840/part784082/784082523/images/big/1.webp'),
    ('677140342', 'https://basket-33.wbbasket.ru/vol6771/part677140/677140342/images/big/1.webp'),
    ('783968430', 'https://basket-36.wbbasket.ru/vol7839/part783968/783968430/images/big/1.webp'),
    ('783968431', 'https://basket-36.wbbasket.ru/vol7839/part783968/783968431/images/big/1.webp'),
    ('783970568', 'https://basket-36.wbbasket.ru/vol7839/part783970/783970568/images/big/1.webp'),
    ('877152767', 'https://basket-39.wbbasket.ru/vol8771/part877152/877152767/images/big/1.webp'),
    ('415796302', 'https://basket-24.wbbasket.ru/vol4157/part415796/415796302/images/big/1.webp'),
    ('890356416', 'https://basket-39.wbbasket.ru/vol8903/part890356/890356416/images/big/1.webp'),
    ('890356418', 'https://basket-39.wbbasket.ru/vol8903/part890356/890356418/images/big/1.webp'),
    ('890356419', 'https://basket-39.wbbasket.ru/vol8903/part890356/890356419/images/big/1.webp'),
    ('758102013', 'https://basket-35.wbbasket.ru/vol7581/part758102/758102013/images/big/1.webp'),
    ('758108753', 'https://basket-35.wbbasket.ru/vol7581/part758108/758108753/images/big/1.webp'),
    ('758132188', 'https://basket-35.wbbasket.ru/vol7581/part758132/758132188/images/big/1.webp'),
    ('758115933', 'https://basket-35.wbbasket.ru/vol7581/part758115/758115933/images/big/1.webp'),
    ('877158122', 'https://basket-39.wbbasket.ru/vol8771/part877158/877158122/images/big/1.webp'),
    ('160480520', 'https://basket-11.wbbasket.ru/vol1604/part160480/160480520/images/big/1.webp'),
    ('160484794', 'https://basket-11.wbbasket.ru/vol1604/part160484/160484794/images/big/1.webp'),
    ('207077618', 'https://basket-14.wbbasket.ru/vol2070/part207077/207077618/images/big/1.webp'),
    ('371992262', 'https://basket-22.wbbasket.ru/vol3719/part371992/371992262/images/big/1.webp'),
    ('411175983', 'https://basket-23.wbbasket.ru/vol4111/part411175/411175983/images/big/1.webp'),
    ('415751271', 'https://basket-24.wbbasket.ru/vol4157/part415751/415751271/images/big/1.webp'),
    ('502522584', 'https://basket-27.wbbasket.ru/vol5025/part502522/502522584/images/big/1.webp'),
    ('504156920', 'https://basket-27.wbbasket.ru/vol5041/part504156/504156920/images/big/1.webp'),
    ('504171392', 'https://basket-27.wbbasket.ru/vol5041/part504171/504171392/images/big/1.webp'),
    ('545148008', 'https://basket-28.wbbasket.ru/vol5451/part545148/545148008/images/big/1.webp'),
    ('16062298', 'https://basket-02.wbbasket.ru/vol160/part16062/16062298/images/big/1.webp'),
    ('366623186', 'https://basket-21.wbbasket.ru/vol3666/part366623/366623186/images/big/1.webp'),
    ('207076111', 'https://basket-14.wbbasket.ru/vol2070/part207076/207076111/images/big/1.webp'),
    ('207086296', 'https://basket-14.wbbasket.ru/vol2070/part207086/207086296/images/big/1.webp'),
    ('207086297', 'https://basket-14.wbbasket.ru/vol2070/part207086/207086297/images/big/1.webp'),
    ('846397846', 'https://basket-38.wbbasket.ru/vol8463/part846397/846397846/images/big/1.webp'),
    ('846397847', 'https://basket-38.wbbasket.ru/vol8463/part846397/846397847/images/big/1.webp'),
    ('877156099', 'https://basket-39.wbbasket.ru/vol8771/part877156/877156099/images/big/1.webp'),
    ('496422555', 'https://basket-27.wbbasket.ru/vol4964/part496422/496422555/images/big/1.webp'),
    ('534368513', 'https://basket-28.wbbasket.ru/vol5343/part534368/534368513/images/big/1.webp'),
    ('695407188', 'https://basket-33.wbbasket.ru/vol6954/part695407/695407188/images/big/1.webp'),
    ('338485315', 'https://basket-20.wbbasket.ru/vol3384/part338485/338485315/images/big/1.webp'),
    ('338506361', 'https://basket-20.wbbasket.ru/vol3385/part338506/338506361/images/big/1.webp'),
    ('366659845', 'https://basket-21.wbbasket.ru/vol3666/part366659/366659845/images/big/1.webp'),
    ('371983282', 'https://basket-22.wbbasket.ru/vol3719/part371983/371983282/images/big/1.webp'),
    ('150610547', 'https://basket-10.wbbasket.ru/vol1506/part150610/150610547/images/big/1.webp'),
    ('159686323', 'https://basket-10.wbbasket.ru/vol1596/part159686/159686323/images/big/1.webp'),
    ('303306021', 'https://basket-18.wbbasket.ru/vol3033/part303306/303306021/images/big/1.webp'),
    ('366639581', 'https://basket-21.wbbasket.ru/vol3666/part366639/366639581/images/big/1.webp'),
    ('366639582', 'https://basket-21.wbbasket.ru/vol3666/part366639/366639582/images/big/1.webp'),
    ('371980424', 'https://basket-22.wbbasket.ru/vol3719/part371980/371980424/images/big/1.webp'),
    ('371980425', 'https://basket-22.wbbasket.ru/vol3719/part371980/371980425/images/big/1.webp'),
    ('468751609', 'https://basket-26.wbbasket.ru/vol4687/part468751/468751609/images/big/1.webp'),
    ('16471980', 'https://basket-02.wbbasket.ru/vol164/part16471/16471980/images/big/1.webp'),
    ('16471981', 'https://basket-02.wbbasket.ru/vol164/part16471/16471981/images/big/1.webp'),
    ('16472033', 'https://basket-02.wbbasket.ru/vol164/part16472/16472033/images/big/1.webp'),
    ('16472035', 'https://basket-02.wbbasket.ru/vol164/part16472/16472035/images/big/1.webp'),
    ('36015336', 'https://basket-03.wbbasket.ru/vol360/part36015/36015336/images/big/1.webp'),
    ('36015858', 'https://basket-03.wbbasket.ru/vol360/part36015/36015858/images/big/1.webp'),
    ('81329861', 'https://basket-05.wbbasket.ru/vol813/part81329/81329861/images/big/1.webp'),
    ('81331482', 'https://basket-05.wbbasket.ru/vol813/part81331/81331482/images/big/1.webp'),
    ('111228462', 'https://basket-07.wbbasket.ru/vol1112/part111228/111228462/images/big/1.webp'),
    ('111228750', 'https://basket-07.wbbasket.ru/vol1112/part111228/111228750/images/big/1.webp'),
    ('111229025', 'https://basket-07.wbbasket.ru/vol1112/part111229/111229025/images/big/1.webp'),
    ('111236986', 'https://basket-07.wbbasket.ru/vol1112/part111236/111236986/images/big/1.webp'),
    ('36016276', 'https://basket-03.wbbasket.ru/vol360/part36016/36016276/images/big/1.webp'),
    ('156202640', 'https://basket-10.wbbasket.ru/vol1562/part156202/156202640/images/big/1.webp'),
    ('156203935', 'https://basket-10.wbbasket.ru/vol1562/part156203/156203935/images/big/1.webp'),
    ('159683497', 'https://basket-10.wbbasket.ru/vol1596/part159683/159683497/images/big/1.webp'),
    ('163667090', 'https://basket-11.wbbasket.ru/vol1636/part163667/163667090/images/big/1.webp'),
    ('177969482', 'https://basket-12.wbbasket.ru/vol1779/part177969/177969482/images/big/1.webp'),
    ('177970528', 'https://basket-12.wbbasket.ru/vol1779/part177970/177970528/images/big/1.webp'),
    ('200796986', 'https://basket-13.wbbasket.ru/vol2007/part200796/200796986/images/big/1.webp'),
    ('207084025', 'https://basket-14.wbbasket.ru/vol2070/part207084/207084025/images/big/1.webp'),
    ('207085537', 'https://basket-14.wbbasket.ru/vol2070/part207085/207085537/images/big/1.webp'),
    ('207085538', 'https://basket-14.wbbasket.ru/vol2070/part207085/207085538/images/big/1.webp'),
    ('207085539', 'https://basket-14.wbbasket.ru/vol2070/part207085/207085539/images/big/1.webp'),
    ('207085540', 'https://basket-14.wbbasket.ru/vol2070/part207085/207085540/images/big/1.webp'),
    ('207085541', 'https://basket-14.wbbasket.ru/vol2070/part207085/207085541/images/big/1.webp'),
    ('207085542', 'https://basket-14.wbbasket.ru/vol2070/part207085/207085542/images/big/1.webp'),
    ('211665983', 'https://basket-14.wbbasket.ru/vol2116/part211665/211665983/images/big/1.webp'),
    ('211665984', 'https://basket-14.wbbasket.ru/vol2116/part211665/211665984/images/big/1.webp'),
    ('238621390', 'https://basket-15.wbbasket.ru/vol2386/part238621/238621390/images/big/1.webp'),
    ('240144261', 'https://basket-15.wbbasket.ru/vol2401/part240144/240144261/images/big/1.webp'),
    ('240144548', 'https://basket-15.wbbasket.ru/vol2401/part240144/240144548/images/big/1.webp'),
    ('240664748', 'https://basket-16.wbbasket.ru/vol2406/part240664/240664748/images/big/1.webp'),
    ('240668162', 'https://basket-16.wbbasket.ru/vol2406/part240668/240668162/images/big/1.webp'),
    ('256594408', 'https://basket-16.wbbasket.ru/vol2565/part256594/256594408/images/big/1.webp'),
    ('256600282', 'https://basket-16.wbbasket.ru/vol2566/part256600/256600282/images/big/1.webp'),
    ('256600393', 'https://basket-16.wbbasket.ru/vol2566/part256600/256600393/images/big/1.webp'),
    ('256600524', 'https://basket-16.wbbasket.ru/vol2566/part256600/256600524/images/big/1.webp'),
    ('256600665', 'https://basket-16.wbbasket.ru/vol2566/part256600/256600665/images/big/1.webp'),
    ('270939308', 'https://basket-17.wbbasket.ru/vol2709/part270939/270939308/images/big/1.webp'),
    ('275019474', 'https://basket-17.wbbasket.ru/vol2750/part275019/275019474/images/big/1.webp'),
    ('275019723', 'https://basket-17.wbbasket.ru/vol2750/part275019/275019723/images/big/1.webp'),
    ('303304049', 'https://basket-18.wbbasket.ru/vol3033/part303304/303304049/images/big/1.webp'),
    ('303304252', 'https://basket-18.wbbasket.ru/vol3033/part303304/303304252/images/big/1.webp'),
    ('366631178', 'https://basket-21.wbbasket.ru/vol3666/part366631/366631178/images/big/1.webp'),
    ('366631179', 'https://basket-21.wbbasket.ru/vol3666/part366631/366631179/images/big/1.webp'),
    ('366631180', 'https://basket-21.wbbasket.ru/vol3666/part366631/366631180/images/big/1.webp'),
    ('448992533', 'https://basket-25.wbbasket.ru/vol4489/part448992/448992533/images/big/1.webp'),
    ('468753428', 'https://basket-26.wbbasket.ru/vol4687/part468753/468753428/images/big/1.webp'),
    ('489541863', 'https://basket-27.wbbasket.ru/vol4895/part489541/489541863/images/big/1.webp'),
    ('489559687', 'https://basket-27.wbbasket.ru/vol4895/part489559/489559687/images/big/1.webp'),
    ('489561590', 'https://basket-27.wbbasket.ru/vol4895/part489561/489561590/images/big/1.webp'),
    ('489562778', 'https://basket-27.wbbasket.ru/vol4895/part489562/489562778/images/big/1.webp'),
    ('489564182', 'https://basket-27.wbbasket.ru/vol4895/part489564/489564182/images/big/1.webp'),
    ('515417265', 'https://basket-27.wbbasket.ru/vol5154/part515417/515417265/images/big/1.webp'),
    ('677151864', 'https://basket-33.wbbasket.ru/vol6771/part677151/677151864/images/big/1.webp'),
    ('677152725', 'https://basket-33.wbbasket.ru/vol6771/part677152/677152725/images/big/1.webp'),
    ('677154302', 'https://basket-33.wbbasket.ru/vol6771/part677154/677154302/images/big/1.webp')
]

OUT_DIR = 'photos'
os.makedirs(OUT_DIR, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'image/webp,image/*,*/*;q=0.8',
    'Accept-Language': 'ru,en;q=0.9',
    'Referer': 'https://www.wildberries.ru/',
}

def download_one(wb_id, url, attempt):
    timeout = [15, 30, 60][min(attempt, 2)]
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read()
    if len(data) < 500:
        raise ValueError(f'файл слишком мал ({len(data)} байт)')
    return data

ok = skipped = failed = 0
fail_list = []

# найти что уже скачано
existing = set()
for f in os.listdir(OUT_DIR):
    if f.endswith('.webp') and os.path.getsize(os.path.join(OUT_DIR, f)) > 500:
        existing.add(f.replace('.webp', ''))

print(f'Уже скачано: {len(existing)} из {len(PHOTOS)}')
print(f'Осталось скачать: {len(PHOTOS) - len(existing)}')
print('-' * 60)

for i, (wb_id, url) in enumerate(PHOTOS, 1):
    if wb_id in existing:
        skipped += 1
        continue
    fname = os.path.join(OUT_DIR, f'{wb_id}.webp')
    last_err = None
    for attempt in range(3):
        try:
            data = download_one(wb_id, url, attempt)
            with open(fname, 'wb') as f:
                f.write(data)
            ok += 1
            last_err = None
            break
        except Exception as e:
            last_err = str(e)[:80]
            time.sleep(1 + attempt * 2)  # 1, 3, 5 сек между попытками
    if last_err:
        failed += 1
        fail_list.append((wb_id, last_err))
    if (skipped + ok + failed) % 20 == 0:
        print(f'  [{i}/{len(PHOTOS)}] новых:{ok} было:{skipped} не вышло:{failed}')
    time.sleep(0.2)

print('-' * 60)
print(f'Готово!')
print(f'  Новых скачано: {ok}')
print(f'  Уже было: {skipped}')
print(f'  Не получилось: {failed}')
print(f'  Всего фото в папке: {len(existing) + ok} из {len(PHOTOS)}')

if fail_list:
    with open('failed_photos.txt', 'w', encoding='utf-8') as f:
        for wb_id, err in fail_list:
            f.write(f'{wb_id}\t{err}\n')
    print(f'\nСписок не скачанных сохранён в failed_photos.txt ({len(fail_list)} шт)')
