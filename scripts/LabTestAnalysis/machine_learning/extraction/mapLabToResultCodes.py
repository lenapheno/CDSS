import sys,os;
from medinfo.db import DBUtil;
from medinfo.db.Model import SQLQuery, generatePlaceholders;
from medinfo.common.Util import ProgressDots;


"""
-- Single join should provide full mapping available, but this is taking very long time with nested sequence scan (<2 hours)
-- Not clear why it isn't taking advantage of order_proc_id index
select proc_code, description, base_name, component_name, count(*)
from stride_order_proc as sop, stride_order_results as sor
where sop.order_proc_id = sor.order_proc_id
group by proc_code, description, base_name, component_name


-- Break out queries to effectively force join as intended



-- Find sample of all orders for lab tests 
-- Assumes that orders with same proc_code will yield same results,
--	but this doesn't work as some lab order_procs don't actually yield respective order_results?
select proc_code, min(order_proc_id), max(order_proc_id), count(*)
from stride_order_proc
where proc_code like 'LAB%'
group by proc_code


-- Find all result components for lab orders (list of sample IDs above)
--	(Don't do a full join on massive tables as ends up with nested sequence scan)
select proc_code, description, base_name, component_name
from stride_order_proc as sop, stride_order_results as sor
where sop.order_proc_id = sor.order_proc_id
and sop.order_proc_id in (489,41040313, 459,41040545, 502,41040465, 544,41040550, 614,41040549, 469,41040433, 458,41040111, 454,41040379, 542,41040031, 556,41040198, 466,41040180, 558,41039856, 688,41039818, 631,39465554, 691,41040197, 481,41037658, 457,41040378, 464,41040102, 680,41000414, 470,41039940, 685,41039816, 532,41038949, 1647,41039793, 1584,41038910, 1109,41040538, 842,41034297, 630,41039372, 1649,41039514, 978,41039792, 1336,41039960, 620,41037376, 786,41039790, 531,41038947, 4070,41040482, 490,41040110, 4061,41039741, 686,41039041, 1160,41040139, 5250,41039962, 2010,41040381, 482,41039676, 13041,41037956, 973,41039898, 551,41039912, 824,41039896, 1001,40777064, 3223,41039795, 2795,41040199, 1815,41038777, 1382,41039618, 1129,41039516, 18854065,41040192, 1553,41028182, 740,41039626, 780,41026004, 1398,41040451, 822,41040540, 486,40803737, 4206,41039623, 1699,41035039, 1123,41034928, 624,41038909, 1005,41039748, 808,41039032, 138299,41039718, 83045,41037186, 2210,41037824, 3997,41039678, 3770,41039889, 3544,41039140, 942,41038393, 982,41035327, 1798,41032078, 15334,40832227, 1554,41019531, 34892,41035427, 714,41034114, 14660,40889482, 1465,41035326, 6532,41040108, 1911,41035092, 11893,41029007, 149099,31221371, 802,41039375, 1138,41037393, 10798,41040204, 629,41034951, 3248,41034994, 534,41039945, 28371580,41038912, 463,41028740, 1576,41039711, 617,40990070, 5316,41025155, 10440,41029125, 29280,41037759, 4190,41022182, 30309,41030976, 1923,41026973, 2244,41037815, 4638,41012350, 5565,41012351, 1397,41036473, 958,40964843, 1378,41032139, 2473,41037660, 3801,41026354, 2856,41034266, 488,39712287, 632,40990835, 4637,41012345, 4236,41000679, 11649275,37985741, 13130,40958309, 799948,41001427, 28123,41033440, 2810,31181974, 5325,41039826, 4897,41039040, 1491,41035087, 628,41034269, 2203,41020341, 65882,41039679, 106627,41036574, 8779,41033143, 2364,41016753, 21286,41029400, 55683,41029248, 8834,41039655, 2963,41026145, 82290,40695443, 2829,41030978, 3378,40788340, 945,41031785, 27919,40989928, 3289,41039990, 7464384,41018354, 10438,41023340, 2552,41027164, 809,41039515, 9893,41028601, 9309,40982877, 31109,41018475, 31485,41035167, 1985,41039144, 16216,40964908, 2353060,41040296, 4938,41003527, 95556,41038768, 2097,40957726, 1753,41018844, 681,40969838, 33963,27630715, 5274,41035242, 2079,41027456, 84035,40691776, 34867,41026763, 43606,40804759, 10740,41039657, 4494895,41037896, 35910,40975445, 10047506,41038868, 11056,40912742, 32853,41006810, 30216,41034454, 616,41037573, 55207,11859867, 11339,27562625, 11330,41026609, 984,41039148, 3004,41012550, 68776,41039376, 505,40976069, 10986,41017588, 17079,41039710, 5006,41011429, 41543,41029214, 76949,25036501, 10488,40967099, 33007,25059099, 118766,41007106, 5324,41040551, 15644,41034167, 5810,40874577, 38459,26952263, 745786,41040279, 20741,41034306, 17272619,41024478, 18219,41026183, 82825,39531502, 786321,40844378, 4735,41034227, 2593,41040073, 120803,41039378, 843481,41012678, 464507,41024482, 5818,40997119, 803,40884839, 18276,31956197, 3989,41036720, 45033,36486040, 10715,40989953, 10946,40750395, 45709,41019210, 1294,10227211, 234537,41010334, 8019,41034997, 2224,2315994, 4648,41035126, 6267,40984856, 8889,41020115, 1965,41010733, 7183,29034693, 734,41039620, 4875610,41037565, 66152,40958832, 30785791,41038989, 249955,41037280, 962,40772888, 35496,41021958, 3796,40747808, 64607,40997655, 5903,14460493, 22186021,41040553, 30729921,40998975, 6573,40802338, 831,29053031, 110335,41030715, 7109,41026338, 11702125,37889153, 930916,41015535, 4223,40929103, 137181,35789584, 454713,40965438, 4572,40716210, 7318,23054883, 69022,40972291, 30258,40864234, 7149,40695752, 4121,40969615, 8043,41026339, 4733,41020753, 938,40721284, 30606,41010417, 2533,41023280, 3968,41040178, 39968,41005647, 155919,40641039, 2964,40668911, 371794,40954938, 101889,41013892, 109690,41030931, 167743,41028128, 38373313,40728658, 39557,40987678, 114845,41012132, 415243,40862274, 2840,40801021, 8261,40781327, 33170,40775266, 20004,41024604, 2298706,40970507, 37830,27506842, 36710,40815369, 12752,40951233, 20097,40965622, 36823,41039874, 783,40979228, 2604,41019263, 141955,35769386, 4521994,40762176, 109591,41039522, 124958,40995073, 14097,27549090, 36574,41039063, 16554,28442709, 29985,40661618, 6427,40872204, 84717,41010613, 1303538,41004310, 19911,41029042, 5222,23073728, 55077,40817633, 205182,40949909, 30941,40658767, 10657,40641211, 437896,40669273, 8208,40926297, 5125255,26232875, 31371,40749606, 32133,40105625, 35155,40902412, 8372580,41013502, 466280,28410622, 6784458,40153682, 169156,40739424, 12202,26951581, 57910,40706917, 110678,40850719, 345774,40525938, 4105,31888589, 26230457,40723112, 1247593,40749563, 38152,40912309, 6231,41014878, 983531,41001093, 15351,13542889, 39225,40754882, 27880,40775169, 34293,40213875, 14443,40860913, 59584,40889514, 3474,11686281, 554558,40990643, 12246993,26220568, 330064,40715389, 23220507,40963261, 74126,41007679, 5542,18151573, 107181,41029026, 202518,40998957, 37438,40770230, 820684,40877307, 35579,40952301, 419770,40967948, 2080,8126935, 382032,41026014, 26238159,41002692, 485921,40693968, 212536,40987928, 62529,40984152, 258038,41028545, 199863,41028525, 17359,40743383, 144685,40824817, 72254,41039709, 124961,40735823, 22677613,40901611, 26881546,40986439, 35775392,40727750, 14069148,41005876, 209192,41039987, 35718462,40711550, 1588991,40902646, 58651,41014879, 29034,40781807, 35814067,40715664, 31395,4515357, 71040,40492163, 11126,41010971, 5616,18189147, 279318,22942089, 120834,41036869, 418205,40899122, 593753,40828680, 103526,40931777, 91266,38176042, 4868,41024795, 226335,40775190, 56860,40725888, 3556,41037572, 11991461,40923628, 15815478,41037657, 5801,41036812, 69204,40824774, 84479,41011627, 12286,41039897, 84655,40797453, 58652,40973375, 113338,40688377, 2476,23059081, 249023,40318881, 44839,3344961, 254598,40343172, 430278,40742558, 2374282,41022121, 35375,20919948, 30063,40559330, 59952,40139949, 58653,41020745, 24485671,40926012, 9057,28471633, 16896,40373051, 28496224,40851171, 424810,40745841, 34548,40709286, 664920,40606887, 177302,29791774, 110008,27576302, 121276,40912395, 16541,40037291, 4143209,6312087, 143694,41018650, 27276420,37960061, 5003,40939124, 1277687,40747035, 484162,36573518, 125069,29069694, 82332,41020746, 221865,25494484, 111904,40764113, 1388,40777376, 590172,40934301, 109939,40809466, 2074998,41028389, 55347,40674931, 110043,36583511, 116327,36658530, 19777692,41037812, 776144,38582745, 436756,40566149, 28233,40851221, 6185,29984933, 26225473,40803688, 112653,40348603, 115060,40534127, 361082,40963417, 65007,41014880, 42045,40749702, 27552884,37904798, 92857,41003157, 6565,40836013, 8402380,40988207, 110906,36502526, 293228,40911753, 3004290,40831683, 1691742,40797713, 167322,41022364, 26175534,40693644, 110907,40800368, 9552,24670668, 27650458,40567536, 789360,41010533, 66838,41007680, 986617,40515770, 3107,40949479, 1750531,41036772, 481198,41028849, 795008,40804632, 3673471,41040273, 41544,40749473, 2680465,40827020, 114045,40961130, 1070476,40804792, 33724,30362738, 25570,40673712, 10045,37795241, 1739006,40777200, 581227,40322579, 73147,41035081, 1401878,34666021, 1938814,37985880, 83091,40695865, 5455480,41036398, 135767,40507725, 95771,40150395, 14004750,40672942, 280604,40558141, 38333,21087251, 57850,40787434, 138975,40634852, 25646191,40672801, 25607215,40917013, 20126,22236392, 260426,40963090, 249180,40921428, 58661,41034354, 1737,40826476, 154595,17237929, 2094039,17969207, 3425213,41039062, 142945,40698561, 18436124,40769252, 98094,40765989, 121774,40728712, 2050330,40619647, 388601,35791823, 2051638,17332157, 2080916,9168480, 2047750,17363905, 2955141,40774892, 112750,40572788, 2940739,40725822, 26932574,37787768, 179109,40315959, 415510,40926254, 2704,40645945, 2918586,40755770, 1493642,40911766, 126262,30851994, 194109,39369092, 470531,40874962, 301904,24104430, 1723555,40267444, 2146025,40860481, 65013,41011433, 2824445,40699803, 9011331,40982238, 1643250,40819518, 5287,40934302, 230526,40694463, 25608062,36291411, 46784,40341369, 30384,40376904, 476042,40554689, 194529,41012006, 19616834,41028544, 1306679,40716140, 164146,40934550, 116815,40874925, 50393,8087954, 175514,40872697, 1586838,40637695, 1312759,40818022, 117521,40863166, 66849,40684913, 1654054,40593605, 110537,40255366, 579954,40804304, 118287,40522306, 422040,40715673, 467372,40937058, 2550233,40807965, 37885932,41028191, 1274364,40456692, 2404333,40068779, 31435271,35194770, 468242,40655839, 194053,40793826, 4325855,40610086, 10255150,40628967, 8601,30989480, 9248486,41010345, 947413,40749638, 62278,40686417, 14123,18043367, 26993211,37908804, 4257,39941985, 718861,40541778, 3397925,41036110, 24458636,40934040, 192966,40232939, 8383556,41011852, 1562815,40872174, 151266,40577760, 113028,40363844, 12575797,37821460, 211640,18036419, 65014,40686418, 474238,33376057, 474376,40591726, 193825,40937297, 10310795,40441462, 255393,39885593, 315220,40573541, 72269,40712631, 35771320,40971540, 982542,40859790, 2632252,40945054, 10181,41026240, 1582786,38126285, 37933678,41005777, 1030662,41006015, 16471,40912261, 30049694,40804606, 1486557,40966397, 26880676,37768617, 72270,40712632, 2871741,40824801, 802160,40604221, 25639156,36300650, 1560206,16974940, 12689,29751219, 2726606,37508825, 306108,40871270, 588033,23047463, 2621919,39465730, 603829,40533361, 79573,40739816, 202789,40658810, 737432,40565139, 710109,41027014, 1291106,40512997, 1591449,16997659, 337052,40390578, 36596590,40872064, 2306402,40737042, 30471676,41028409, 469920,40555483, 206993,40829110, 12044867,40745859, 1950356,40620912, 35752998,40958210, 196655,40877575, 1384729,40519807, 647732,40560329, 22747595,40770225, 25550951,40817934, 527673,41025420, 667356,40534049, 2378066,36578670, 710335,40525989, 279969,23113528, 216718,40991060, 86692,38799017, 3356188,40823308, 66855,40724079, 13514901,40631857, 36741939,40928343, 24701,18641100, 1389131,40224048, 1068060,40998509, 711533,38527882, 194727,37735656, 1991119,40697548, 253618,20892442, 629375,40666760, 785375,40507133, 27560526,40803618, 141959,23037011, 4604434,40987569, 170205,39230490, 191741,40190444, 38155,39746168, 75907,40724080, 257472,39745275, 474943,39665643, 1232843,38901382, 25385437,37503332, 309409,18678215, 137117,40553152, 3407274,40858220, 176344,39496300, 1380732,40877577, 715179,35561169, 2101589,40929525, 18250124,41033936, 128488,39168876, 38642,32919531, 2541934,40932778, 1961,40721381, 1938,899811, 5748973,40830600, 69544,40792659, 3847164,40110928, 3228998,40210142, 58968,40604816, 2373943,40912919, 338044,8163732, 2873580,26413953, 171233,5095899, 177370,39481721, 58670,40794180, 1357915,17180521, 281552,40524035, 41191,40936989, 1638992,40734419, 33942,39339823, 22251028,40885229, 4561273,40982213, 499632,40853155, 28332,23893030, 257236,40219532, 7380920,40383942, 9585854,40744203, 2577753,28955954, 480697,34531307, 1587318,40425056, 34205,17056656, 579184,40501343, 1555317,40693902, 59096,39601114, 437256,41033218, 4313549,40639215, 5197023,26098120, 62286,40491241, 64351,40547141, 10403,40650903, 197445,39869994, 166939,40707738, 116405,40776662, 2688264,40961373, 328974,40855111, 95039,15081094, 27777449,40901089, 2209519,40284457, 2082774,40776389, 277584,16722128, 115431,40078236, 492981,41020751, 85522,40797571, 3592997,40221911, 2272582,34816799, 511637,40276568, 824571,40664879, 2647665,11368310, 113212,40912723, 1243868,39787298, 1201631,40184819, 3109971,40205830, 2756061,39346583, 243143,40230023, 2084645,41020628, 547932,36523775, 31340072,40506574, 73170,40508365, 2684984,40839740, 2004975,40655899, 274844,39823899, 1924514,40547461, 277125,40583080, 1229885,40518907, 171259,40748189, 656228,39818383, 192577,39330824, 170224,40688252, 333756,40773112, 6822,40645991, 2051639,41007570, 555628,40368804, 247133,40984050, 3925568,41027340, 170204,39204462, 333850,40803865, 1483502,39734446, 18577794,40382225, 548396,40685796, 3069685,40958850, 2525236,25063799, 12625,39937209, 670067,40801806, 740146,38173523, 713838,40583726, 219733,14411572, 579497,40368806, 2184307,39530948, 28398689,40111822, 26453,34244695, 11897309,36833016, 276163,40611461, 6840090,39104711, 172345,13690914, 25612577,36109031, 578746,40390183, 5343,1935087, 247241,37417773, 618,915908, 100180,40718674, 1175111,40644590, 521333,40251064, 1215122,39796152, 58777,40700749, 443415,38100282, 3141313,39806551, 1319360,40214158, 40525,35024822, 145302,39573789, 115910,10793828, 17747,26694079, 703048,40456709, 5952598,40664189, 411942,40518997, 8047690,40970294, 2256161,33364482, 258364,40508166, 801849,40770183, 595007,40345029, 4206206,27583542, 1148697,23101605, 3055373,40588258, 2928775,40977588, 250893,40746084, 2651908,40409223, 237980,39239406, 3086822,40746042, 2525815,11034534, 63442,40623349, 93145,1061360, 508276,40616868, 283185,40641864, 3542254,30430162, 474766,40437588, 879333,40390184, 1827972,39930820, 36559091,40823450, 437554,10625662, 251323,40474888, 2858597,41020632, 5159502,40634292, 411251,40364868, 492693,41018450, 884467,40390185, 1255370,40510657, 1488191,38867360, 11471,13107169, 250774,40713056, 656600,40608183, 303723,40612103, 38291427,40885784, 712613,39362147, 279344,39531091, 39460427,40964929, 2034,39508744, 830708,33298329, 11920263,36823012, 1177108,37519038, 992539,40371120, 301834,38223185, 1149975,25593010, 199047,40648321, 21682102,40899730, 356471,38493735, 797190,39706351, 1041279,38175995, 494491,39975473, 10171477,34274728, 2701734,39487823, 670632,41037953, 484480,39335468, 3030158,40341112, 15172,927107, 3113232,13595473, 3813835,37594216, 9159,40526608, 1940515,40236083, 995420,40122493, 995419,40118277, 1296860,22385236, 2830,1608138, 384917,38881106, 1997486,36471031, 3089093,39986266, 3306898,40612254, 956513,40669187, 9693387,41010408, 413667,39536441, 38307894,40964891, 29906,1501018, 410288,16173676, 2363797,40914607, 2677471,40498671, 1002500,40159819, 1746211,39765814, 3579984,40621343, 4180988,39443310, 5365137,39804204, 469125,37987200, 443147,38471654, 929116,39362677, 1429291,40201500, 33866,39914137, 2654693,40181366, 364213,39885966, 858329,36408073, 25713968,39352642, 3327368,39670616, 938171,39438691, 300560,39361437, 995425,40235058, 6893277,39938149, 266253,40477182, 2348717,39146214, 2568767,40769800, 24880427,40593731, 15460608,39346697, 8961679,40016224, 3532813,24830511, 114605,28108735, 3140786,39822349, 506619,40111015, 3762392,40957489, 683958,40961425, 5437847,34511778, 1509113,36169757, 1718899,40556766, 444732,39882082, 332131,40876386, 1720754,40715633, 828127,28034044, 36596576,40799091, 3218618,26656268, 2457262,35006408, 984523,40159173, 2463989,36196994, 10123467,40938665, 36939872,40837301, 3001185,40690221, 2099167,40970562, 1068756,38978559, 23485356,34064124, 723017,40574888, 292933,16422485, 2076405,37575054, 848283,33488058, 983541,40178684, 1705453,38528570, 171779,39856572, 823864,39878401, 38039334,40824802, 1411333,40695451, 1754914,40316456, 31331020,39909607, 1393095,39090745, 221847,34740518, 1012798,40141202, 2152264,39260468, 2997693,39637145, 2510433,11037054, 2785043,39200757, 3103821,36957421, 935510,40362336, 35435110,40963207, 200769,40935260, 20947291,40804131, 1729546,40648334, 4425313,38710398, 2128551,40341291, 2377337,34352441, 3467337,38618006, 967485,40422927, 956519,38240966, 941957,38233636, 85294,1561821, 5756279,24187500, 478294,13047223, 2838555,40227902, 14840016,40206426, 1322805,39965639, 1000788,40173954, 56238,1952622, 14976847,39453717, 2132270,38159078, 2465,906048, 10999501,40581178, 9461072,40525990, 32962797,40980698, 28206667,40824762, 2216754,40898401, 2554149,41036729, 1032812,40144400, 2674621,26746453, 630724,40480200, 823865,39802344, 5360,1596947, 3512053,37877578, 475249,36861010, 1028,1512376, 316375,8023183, 34742891,40925427, 505382,17259845, 114063,40932341, 605720,15792556, 2514727,39256470, 2132269,38172702, 3430257,38954052, 325768,39747788, 3221424,39834571, 723602,20214258, 2466,870592, 1252880,38586560, 356119,39509232, 915968,37975544, 610140,33154295, 29029328,40827017, 743560,40261955, 111035,27046757, 1512205,39236985, 120463,35394192, 547199,40203464, 28175,37829422, 1738638,40674883, 252617,34056355, 606042,10063531, 7585737,40773179, 2508844,16066443, 23606647,31720058, 4062710,40212381, 24502112,38628820, 1831703,40695810, 221068,34844613, 551755,36466456, 1007464,40659633, 12254751,26167399, 164318,1592490, 805605,38894710, 4100120,40173955, 306654,40577736, 4122446,40141233, 11875,35325677, 952691,39442202, 24452541,39477578, 823,1590645, 988376,29650588, 26906996,40381998, 2959863,39150978, 330720,35116743, 3669270,40696534, 4087717,40176529, 113193,2417635, 1259380,39459167, 1023457,38334078, 32920,39935444, 710021,38628780, 4105691,40206436, 1404618,40450058, 24441027,40904163, 587971,38518678, 12741,839577, 2164310,37984946, 20156428,38007206, 235439,39556984, 40234,1468413, 164592,37540116, 472631,1449255, 2678227,40356567, 46436,35122033, 1217325,36624516, 3305628,37790281, 11460690,39549912, 2243457,38286627, 628006,40612141, 19062685,40716057, 4128072,40227910, 36584308,40639262, 554576,36447634, 494191,40294476, 467449,40723321, 1770708,36094315, 4317,1739194, 1673139,32404115, 15257097,40674804, 387354,40240449, 438529,40093519, 260117,1583198, 26853595,40477065, 4875966,39689680, 84447,40406935, 792766,40566787, 30715506,40963050, 26474049,40781805, 24446388,37973088, 1159403,36705060, 19324115,39874099, 2564407,39364361, 1934067,36888264, 4436264,39656103, 221472,39884181, 4086797,40289021, 18468383,37519393, 1638774,39093302, 2941096,30746383, 11729607,40151987, 3847258,34139835, 6451,40407544, 35989254,40387820, 447497,8590030, 30613,1604364, 4962986,36786373, 6901737,39415580, 824272,31716754, 620611,39466956, 141075,37187609, 5422220,40002843, 27092311,41033173, 2873428,38794448, 20429482,40506045, 9211046,40729032, 384904,1522810, 1210718,39714122, 1727694,38897845, 27676940,40067604, 7677672,40083897, 3420363,35296172, 10245838,37329569, 28676635,39548003, 16517269,39911396, 27510445,40707615, 1915468,32228438, 35735090,40917480, 2381983,39366423, 3297385,40431628, 4929898,40219494, 2975916,37947902, 2374808,37465210, 4083353,40167598, 28345109,41024178, 7095265,40608283, 280526,11725017, 876579,37518819, 1072790,39736588, 18292205,39646894, 267129,38665555, 4109614,40172196, 2238706,39264286, 1173433,38880304, 4085962,40204254, 5748846,40336533, 257824,39423191, 28685751,39528882, 166766,22532113, 4928936,40194195, 1770240,40287309, 4109615,40289022, 8660395,37322724, 6402295,40576524, 4144904,39910293, 1037756,38551071, 2756241,13010307, 1555781,34352440, 3058058,38858935, 3811147,38448263, 1410351,31818947, 532823,30530030, 9302312,38982954, 2673670,32108922, 3351592,13024640, 2009932,6121040, 498350,39559155, 32537198,37978804, 17000,1557329, 229655,38879516, 18721423,37577525, 23922545,34340894, 8247432,24945754, 547900,35336674, 3732488,34833450, 6519457,35586934, 4118269,40172197, 1009803,34272605, 8139421,40773081, 5410789,39878857, 384764,40231521, 718741,40445298, 21289334,39412710, 99256,1451012, 88063,28441245, 337082,33013581, 4766298,32423999, 1015550,31269492, 7136562,39991300, 248838,39599840, 58260,36630820, 4838667,39750151, 14204304,40912178, 664801,36494327, 23036801,40612140, 3896099,36052756, 4360740,37720495, 3305801,40086106, 739484,37339911, 11917321,27982338, 16486685,32237389, 448818,37065513, 554008,25829579, 4085963,40187613, 485756,32516943, 955166,30066205, 413353,38244335, 3516242,39577536, 19932662,40636021, 8363685,38786382, 28066984,39520482, 5998576,36090312, 698323,35026760, 1586986,38881105, 1017556,23089043, 4103287,40172198, 1183487,38575839, 24151320,40585214, 4093934,40227912, 1887695,40587105, 11323621,37392747, 2254171,22073558, 7770390,39649542, 1434078,39498864, 33431175,40406934, 12603879,25581402, 16453096,40695532, 1016789,39992610, 10705396,37193136, 303724,34486749, 527212,38203412, 335234,7692736, 6716171,40829039, 85724,1472281, 13197,30978156, 4096788,40206438, 364704,5055397, 37040,1595818, 3276787,38909159, 4095043,40198374, 22751449,40042171, 16451217,40926063, 30609321,40344202, 2581069,37506499, 19130352,40095451, 4092860,40185188, 3515842,28667515, 5331999,5800633, 1828472,29337692, 30704824,40522613, 1727760,39713917, 9669564,35088027, 3566480,28040612, 8444967,34022706, 11880780,41036728, 1564,912363, 30582453,38534085, 27141630,41029626, 29928,2181293, 8368078,30522935, 2999476,37937288, 7330962,40869494, 5220813,24668097, 3543103,38295740, 30285570,39855816, 20484947,40384451, 1902,1553548, 4523232,37909806, 2551450,35939189, 4365047,23482721, 6097815,39582976, 9015284,26429331, 1216544,40664270, 4088272,40195198, 938425,36826296, 4388863,28006707, 111202,1247236, 384285,38405361, 491300,4565603, 4124350,40187614, 7857373,40200980, 1790767,29750921, 38477899,41031186, 1664186,29460683, 12199710,37460913, 268836,39401440, 12016317,36917191, 198812,1539049, 11134492,40686132, 822213,9291747, 146010,1494874, 3053962,35922559, 67064,715570, 5244254,19523487, 3684226,39937204, 657723,4159204, 464525,1058708, 4938238,11669102, 38573908,40936988, 14607374,27603040, 26231463,39035575, 743572,22105311, 15182270,39892303, 12411752,29133612, 3300291,10543632, 6108736,40655947, 4086808,40204256, 5761758,26262880, 1433685,7687969, 10863116,30395791, 5075237,16035255, 2636225,39903223, 15042328,38406532, 26193513,39523295, 22905037,38315882, 20921536,32385656, 303557,12568050, 16476098,40008140, 16620680,40912907, 147057,38879813, 3888518,38656612, 4508347,36028523, 29187343,38854693, 3475514,29745147, 13984137,14388592, 4257327,10596028, 4105016,40166330, 367339,4566900, 8774506,39219488, 67743,2472194, 38662525,40722800, 4138310,40206440, 2135142,7914157, 762041,35655206, 12657218,40936112, 3538779,33953366, 25779493,40738692, 7275903,40291334, 2952219,33312744, 27214018,40126551, 3236535,33112134, 14566525,24454262, 777576,21994971, 24921667,40223180, 960052,36027196, 17227621,31167200, 11901594,21191748, 35733990,36199854, 15219893,39628959, 1428568,27657850, 5834069,38685583, 16261,36875570, 2319532,18753392, 24271305,36813499, 27920459,38431143, 4096800,30774523, 4096799,30781508, 45187,1526170, 31008599,37854588, 27588442,31637369, 4115427,30740999, 11178840,37314360, 4320329,39379459, 24494079,29824815, 16159466,36727562, 8499021,35194034, 2944971,38582222, 4172093,20512803, 4122471,30762500, 7912,912040, 2954026,38582223, 276164,1589766, 3356356,28652032, 2375647,28194290, 5581825,21660931, 3488613,15951764, 35379105,40094617, 16536263,38810511, 750269,18377693, 5752703,30362561, 30072078,36620798, 19887494,40951430, 1912226,40023927, 4875144,31475387, 33552001,34910046, 9694256,30528669, 18578059,38283559, 851764,27360184, 5800656,27041813, 2727333,18172310, 2646420,9509070, 10752641,32449037, 360736,25651064, 35856820,40067675, 20373206,30532254, 113767,33447286, 3832392,37690297, 302911,11773086, 38287580,40326512, 6117049,25642084, 28008484,31590255, 1426486,7687968, 609735,16155112, 6750422,30710113, 6810053,26537293, 6714466,30769120, 33550669,36520783, 5003212,36718383, 1050029,34198824, 28002141,39503940, 28696204,34723586, 20077393,39804398, 20345807,27285502, 6723601,30877851, 301828,29582729, 8061378,39245717, 15431628,37848566, 11562247,29843919, 1052341,37981339, 2511149,15276127, 10859958,29506464, 1884242,26201496, 684719,34946891, 4077291,36197803, 410040,1477071, 4419562,20517319, 36905447,40325527, 25111548,38154324, 7140269,36214119, 3351425,31938668, 12265610,33882441, 23499910,32259889, 201336,1575939, 19239065,23153117, 1465242,38505811, 6707929,30763576, 6698620,30859536, 15185269,37765059, 1187972,25977518, 11296736,17402977, 2012976,39916631, 12850962,15954549, 6675665,30912052, 1286924,22548972, 31709735,33703038, 31815378,40618408, 20688186,31426132, 25578528,39764140, 25010916,38423694, 3002905,10634226, 5231683,36921803, 4673345,34748435, 19635484,32375671, 24365494,33852434, 8098012,34621740, 36638525,38857587, 274711,1607769, 10081949,40077812, 13844024,28982480, 8918926,26058385, 9433018,34485688, 32851,1492617, 1434079,39271413, 11481631,23418518, 11133512,38989325, 28437931,28505824, 6557882,37179393, 934575,1591063, 2886890,5877173, 409954,8834312, 2837952,34942399, 30116663,36351417, 19442277,19741152, 11998847,28521369, 9988594,38964249, 793808,32453189, 1325306,38009300, 2242312,14863888, 6697678,30883982, 6000324,17588262, 557900,807785, 9535158,31580249, 6711156,30890296, 9340871,39894178, 1213345,21708651, 21963485,22614043, 9416073,26016717, 10743687,25450735, 7937870,31179044, 3387140,29885898, 28997484,41011302, 29187006,29605904, 288666,1155969, 28463876,39859719, 20417427,30408395, 32581129,39771561, 6719686,30883983, 38453563,38533099, 31032681,39509611, 12462214,40287870, 1558904,22728402, 3544581,28534277, 553309,12743545, 4535524,28679225, 21579348,39834076, 4525578,35755077, 6697679,30883984, 25446745,29425879, 23819737,34545142, 5996393,19086055, 122230,733619, 36395339,39897067, 14505613,14681847, 3999825,25881686, 26560101,37352284, 26466500,36063515, 27652979,40565324, 10884047,13127554, 16652625,38222736, 27390240,33527532, 33601567,36134106, 22560311,22635932, 4960197,24154230, 35063262,40016911, 17328434,33066357, 11919372,22024492, 13273581,16889200, 10216088,21363692, 4718218,20107999, 5973258,19004996, 6533887,8239500, 27270409,30474159, 16104423,25112712, 4722288,14431261, 986491,1544276, 8498339,13870566, 7990417,22587759, 565611,1556663, 16167481,25704083, 17545094,19593259, 6347527,40077996, 26738461,37964421, 29467186,35175310, 28780359,28862623, 580028,40303910, 14157509,16058938, 32133375,36683544, 17812593,40553099, 4925577,10636616, 13641061,40132846, 4910682,10607105, 9765892,28721654, 1539980,29052753, 33166663,35111594, 3190395,16327225, 290543,1470913, 11181509,32035905, 3061239,4564956, 34292923,36109600, 29275425,35912276, 39646851,40863888, 3827810,33467509, 12103678,40455275, 607246,1243694, 27063,24040959, 2212997,2251834, 28918168,29003587, 1610041,2833929, 32296105,32642722, 17923518,37677512, 25727901,25796783, 24009379,31807199, 11862905,11954854, 32976530,39138991, 19253835,19710239, 12755405,39428821, 15854629,26167287, 191547,208754, 9396418,32307108, 9263857,9493061, 8686063,13703467, 1316131,1331937, 11919816,11958575, 2021197,2061713, 27768674,27899290, 8145767,8182061, 11189586,32633390, 22371180,38903462, 956446,1006586, 7186549,7209036, 35750302,37124481, 13849883,13874580, 1746978,3489636, 14968972,21749917, 941888,1554553, 33709271,33755020, 24573685,36701777, 470822,1539050, 2053252,38089070, 12053495,28704990, 40416060,40446487, 12186556,25312355, 33619306,33678047, 39573210,39902262, 34961127,35104116, 1213519,3859938, 38948617,39327793, 23894325,26812326, 12032629,21403841, 40489163,40574117, 38971045,39785871, 36867172,40096273, 3475,37650463, 960545,1192005, 17332849,17472834, 40948379,40993419, 271564,1247973, 1589547,21804057, 956514,1190270, 25715428,25755605, 27990780,29802163, 3733295,29027414, 18146605,21301738, 40892696,40990606, 16896499,22067127, 1302366,1343118, 4223200,4254008, 719648,783282, 15166192,19028183, 824237,995157, 28433845,32524539, 12937302,23827659, 8911315,8933822, 23038424,23374333, 34945149,38507536, 3385064,3752369, 17660726,26976951, 3472436,3492554, 22776542,29255933, 362352,12019613, 3874193,26903621, 28840850,38553421, 9034844,9164913, 590249,3453620, 223328,2856547, 16025355,17045732, 32489957,37778659, 40075917,40409296, 38287579,38622395, 39739615,39791492, 8905667,8956346, 15178250,24685739, 11736171,12723000, 22659818,36786565, 36746005,36772128, 966574,1199653, 303081,1989873, 23576896,38436314, 15503974,33240293, 5698636,5724456, 36668387,38638930, 10802242,25346054, 6704992,30890297, 29069075,32266960, 23146992,31644245, 16101180,16204988, 24498714,27309844, 660024,938551, 35761535,40281642, 27342789,28791601, 8787042,39962403, 36751777,40263274, 32222051,32897827, 28622887,34995703, 3679994,3697677, 28366926,28430541, 35940588,35958794, 342606,348964, 28412,42973, 10284774,10337827, 24037346,24043535, 19307377,19329661, 11330496,11330497, 6699565,6710042, 37605884,37688088, 23984359,24024438, 24288716,24348923, 1263717,1263718, 40272721,40338496, 18298676,18377685, 37605885,37634693, 37620730,37639037, 38878116,39021327, 21910169,21980370, 35615382,35625738, 6432099,6468746, 27835033,27845565, 19733315,19753548, 40576597,40588786, 37288609,37289901, 36935872,36947319, 40180,46636, 22861157,22936706, 3002938,3044899, 6720902,6729384, 17643771,17726285, 29682605,29717020, 37822373,37867159, 6079369,6088999, 15183740,15184584, 27454997,27480318, 19367280,19424847, 33111953,33122339, 37594907,37665145, 23837645,23911427, 1124313,1127285, 36594657,36602199, 27213149,27301823, 32988989,33041131, 27503909,27505647, 17626489,17674261, 5583139,5633667, 309068,320637, 6511416,6511417, 24392236,24395529, 23361720,23421153, 32615701,32644576, 3640026,3661934, 6707930,6735425, 37562188,37562810, 29048077,29079862, 328336,341223, 16002906,16026928, 3390961,3427445, 40033952,40129009, 2161518,2202100, 800383,805927, 2842766,2851898, 4824395,4848113, 20008272,20018054, 254992,255770, 31705801,31740215, 39701092,39829861, 23000854,23080727, 25200665,25269428, 39004110,39019662, 1192767,1212135, 39649876,39740543, 982893,1008558, 18305538,18375888, 39329204,39412719, 363981,368544, 202784,218391, 6720901,6750425, 773634,788451, 9613943,9649304, 998513,999284, 6701345,6714467, 5550030,5556810, 19765469,19818152, 17049204,17075562, 31727082,31737679, 29703197,29735052, 40056378,40147809, 22408338,22418702, 31424559,31458903, 15245821,15279416, 17341669,17351228, 128699,128700, 2214094,2248886, 16316536,16395388, 37612848,37624120, 30052033,37236091, 5614817,5650282, 33437125,33440012, 7991751,7991752, 32882060,32920283, 26155617,26226656, 23835163,23859626, 36451954,36536952, 40910939,40916406, 6699566,6711157, 17325710,17347605, 6810055,6853956, 39785340,39830775, 17340852,17348318, 37505641,37619713, 26909141,26921056, 3901281,3921210, 29394546,29431471, 7768528,7769335, 3390960,3393218, 38917520,38984909, 35516450,35564639, 27310546,27315309, 8347820,8377436, 14055685,14080544, 4337350,4415274, 31598312,31680617, 33040652,33044100, 28554311,28579672, 22981880,23000628, 40284609,40290631, 34915160,34940274, 11630490,11630490, 1028611,1028611, 39633085,39633085, 2616926,2616926, 2616927,2616927, 26224755,26224755, 32068676,32068676, 1551329,1551329, 35782101,35782101, 29831767,29831767, 38632136,38632136, 12383939,12383939)
group by proc_code, description, base_name, component_name
"""

# Number of result items to sample to look for respective lab orders
#	Without this, would be joining on potentially 10,000s per each result item?
SAMPLE_SIZE = 100;

prog = ProgressDots(total=37500100);

print("proc_code\tdescription\tbase_name\tcomponent_name")

conn = DBUtil.connection();
cursor = conn.cursor();

query = """
	select order_proc_id, base_name, component_name
	from stride_order_results
	order by base_name
	"""

cursor.execute(query);

lastBaseName = None;
lastComponentName = None;
orderProcIds = set();
nIds = 0;

row = cursor.fetchone();
while row is not None:
	(orderProcId, baseName, componentName) = row;

	if baseName != lastBaseName and nIds > 0:
		# Moving on to base name. Sub-query for the last one now
		print(lastBaseName, lastComponentName, file=sys.stderr)
		subQuery = """
			select proc_code, description, count(order_proc_id)
			from stride_order_proc
			where order_proc_id in (%s)
			group by proc_code, description
			""" % generatePlaceholders(nIds);
		subResults = DBUtil.execute(subQuery, tuple(orderProcIds), conn=conn);
		for procCode, description, count in subResults:
			print(str.join("\t", [procCode, description, lastBaseName, lastComponentName]));

		orderProcIds.clear();	# Reset once done
		nIds = 0;

	lastBaseName = baseName;
	lastComponentName = componentName;
	if nIds < SAMPLE_SIZE:	# Don't track all, just the first sample
		orderProcIds.add(orderProcId);
		nIds += 1;

	row = cursor.fetchone();
	prog.update();


# Final base name to query off of
subQuery = """
	select proc_code, description, count(order_proc_id)
	from stride_order_proc
	where order_proc_id in (%s)
	group by proc_code, description
	""" % generatePlaceholders(nIds);
subResults = DBUtil.execute(subQuery, tuple(orderProcIds), conn=conn);
for procCode, description, count in subResults:
	print(str.join("\t", [procCode, description, lastBaseName, lastComponentName]));

prog.printStatus();