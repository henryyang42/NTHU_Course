# -*- coding: utf-8 -*-

week_dict = {'M': 'a', 'T': 'b', 'W': 'c', 'R': 'd', 'F': 'e', 'S': 'f'}

course_dict = {'1': 'a', '2': 'b', '3': 'c', '4': 'd', 'n': 'e', '5': 'f',
               '6': 'g', '7': 'h', '8': 'i', '9': 'j', 'a': 'k', 'b': 'l',
               'c': 'm'}


cou_codes = ['ANTH', 'ANTU', 'ASTR', 'BME ', 'BMES', 'CF ', 'CFGE', 'CHE ',
             'CHEM', 'CL ', 'CLC ', 'CLU ', 'COM ', 'CS ', 'DL ', 'DMS ',
             'ECON', 'EE ', 'EECS', 'EMBA', 'ENE ', 'ESS ', 'FL ', 'FLU ',
             'GEC ', 'GE ', 'GEU ', 'GPTS', 'HIS ', 'HSS ', 'HSSU', 'IACS',
             'IACU', 'IEEM', 'IEM ', 'ILS ', 'IMBA', 'IPE ', 'IPNS', 'IPT ',
             'ISA ', 'ISS ', 'LANG', 'LING', 'LS ', 'LSBS', 'LSBT', 'LSIP',
             'LSMC', 'LSMM', 'LSSN', 'LST ', 'MATH', 'MATU', 'MBA ', 'MI ',
             'MS ', 'NEMS', 'NES ', 'NS ', 'NUCL', 'PE ', 'PE1 ', 'PE3 ',
             'PHIL', 'PHYS', 'PHYU', 'PME ', 'QF ', 'RB ', 'RDDM', 'RDIC',
             'RDPE', 'SCI ', 'SLS ', 'SNHC', 'SOC ', 'STAT', 'STAU', 'TE ',
             'TEG ', 'TEX ', 'TIGP', 'TL ', 'TM ', 'UPMT', 'WH ', 'WW ',
             'WZ ', 'XA ', 'XZ ', 'YZ ', 'ZY ', 'ZZ ', 'E ', 'W ', 'X ']


DEPT_CHOICE = (('', '開課代號 Choose the course offering department'),
               ('GE', 'GE  　通識教育中心 General Education'),
               ('GEC', 'GEC 　通識核心 General Education Core Courses'),
               ('ANTH', 'ANTH　人類所 Anthropology'),
               ('ANTU', 'ANTU　人類所與交大合作課程 Anthropology and NCTU'),
               ('ASTR', 'ASTR　天文所 Astronomy'),
               ('BME', 'BME 　生物醫學工程研究所 Biomedical Engineering'),
               ('BMES', 'BMES　醫環系 '
                +'Biomedical Engineering and Environmental Sciences'),
               ('CF', 'CF  　大學中文 College Chinese'),
               ('CFGE', 'CFGE　共同教育委員會 '
                +'Commission of General Education'),
               ('CHE', 'CHE 　化工系 Chemical Engineering'),
               ('CHEM', 'CHEM　化學系 Chemistry'),
               ('CL', 'CL  　中文系 Chinese Literature'),
               ('CLC', 'CLC 　華語中心 Chinese Language Center'),
               ('CLU', 'CLU 　中文系與交大合作課程 '
                +'Chinese Literature and  NCTU'),
               ('COM', 'COM 　通訊所 Communications Engineering'),
               ('CS', 'CS  　資工系 Computer Science'),
               ('DL', 'DL  　遠距課程 Distance Learning'),
               ('DMS', 'DMS 　醫學科學系 Medical Science'),
               ('E', 'E   　工學院 College of Engineering'),
               ('ECON', 'ECON　經濟系 Economics'),
               ('EE', 'EE  　電機系 Electrical Engineering'),
               ('EECS', 'EECS　電資院學士班 Undergraduate Program '
                +'of Electrical Engineering and Computer Science'),
               ('EMBA', 'EMBA　高階經營管理碩士班 '
                +'Executive Master of Business Administration'),
               ('ENE', 'ENE 　電子所 Electronic Engineering'),
               ('ESS', 'ESS 　工科系 Engineering and System Science'),
               ('FL', 'FL  　外語系 Foreign Languages and Literature'),
               ('FLU', 'FLU 　外語系與交大合作課程 '
                +'Foreign Languages and Literature and NCTU'),
               ('GEU', 'GEU 　通識中心與交大合作課 '
                +'General Education and NCTU'),
               ('GPTS', 'GPTS　台灣研究教師在職進修 '
                +'Graduate Program of Taiwan Studies for In-service Teachers'),
               ('HIS', 'HIS 　歷史所 History'),
               ('HSS', 'HSS 　人社院學士班 Interdisciplinary Program '
                +'of Humanities and Social Sciences'),
               ('HSSU', 'HSSU　人社學士與交大合作課 Humanities and '
                +'Social Science &amp; NCTU'),
               ('IACS', 'IACS　亞際文化碩士學程 International Program in '
                +'Inter-Asia Cultural Studies (University System of Taiwan)'),
               ('IACU', 'IACU　亞際文化與台聯大合作 International Program in '
                +'Inter-Asia Cultural Studies (University System of Taiwan)'),
               ('IEEM', 'IEEM　工工系 Industrial Engineering and '
                +'Engineering Management'),
               ('IEM', 'IEM 　工工系碩士在職專班 Industrial Engineering and '
                +'Engineering Management (Engineering Professional '
                +'Master Program)'),
               ('ILS', 'ILS 　學習科學研究所 Learning Sciences'),
               ('IMBA', 'IMBA　IMBA International Master of '
                +'Business Administration'),
               ('IPE', 'IPE 　工學院學士班 '
                +'Interdisciplinary Program of  Engineering'),
               ('IPNS', 'IPNS　原科院學士班 Interdisciplinary Program '
                +'of Nuclear Science'),
               ('IPT', 'IPT 　光電所 Photonics Technologies'),
               ('ISA', 'ISA 　資應所 Information Systems and Applications'),
               ('ISS', 'ISS 　服務科學所 Service Science'),
               ('LANG', 'LANG　語言中心 Language Center'),
               ('LING', 'LING　語言所 Linguistics'),
               ('LS', 'LS  　生科系 Life Science'),
               ('LSBS', 'LSBS　生資所 Bioinformatics and Structural Biology'),
               ('LSBT', 'LSBT　生技所 Biotechnology'),
               ('LSIP', 'LSIP　生科院學士班 Interdisciplinary Program '
                +'of Life Sciences'),
               ('LSMC', 'LSMC　分生所 Molecular and Cellular Biology'),
               ('LSMM', 'LSMM　分醫所 Molecular Medicine'),
               ('LSSN', 'LSSN　系神所 Systems Neuroscience'),
               ('LST', 'LST 　科法所 Law for Science and Technology'),
               ('MATH', 'MATH　數學系 Mathematics'),
               ('MATU', 'MATU　數學系與交大合作課程 Mathematics &amp; NCTU'),
               ('MBA', 'MBA 　經營管理碩士班 Master '
                +'of Business Administration'),
               ('MI', 'MI  　軍訓 Military Education'),
               ('MS', 'MS  　材料系 Materials Science and Engineering'),
               ('NEMS', 'NEMS　奈微所 NanoEngineering and MicroSystems'),
               ('NES', 'NES 　核工所 Nuclear Engineering and Science'),
               ('NS', 'NS  　原科系 Nuclear Science'),
               ('NUCL', 'NUCL　原科院'),
               ('PE', 'PE  　體育 Physical Education'),
               ('PE1', 'PE1 　大一體育 Physical Education'),
               ('PE3', 'PE3 　體育(校隊) Physical Education'),
               ('PHIL', 'PHIL　哲學所 Philosophy'),
               ('PHYS', 'PHYS　物理系 Physics'),
               ('PHYU', 'PHYU　物理系與交大合作課程 Physics and NCTU'),
               ('PME', 'PME 　動機系 Power Mechanical Engineering'),
               ('QF', 'QF  　計財系 Quantitative Finance'),
               ('RB', 'RB  　輻生[1998.6以前]'),
               ('RDDM', 'RDDM　半導體元件及製程專班 Industrial Technology '
                +'R&amp;D Master Program on Semiconductor Devices &amp; '
                +'Manufacturing Process'),
               ('RDIC', 'RDIC　積體電路設計專班 Industrial Technology '
                +'R&amp;D Master Program on IC Design'),
               ('RDPE', 'RDPE　產業研發碩士電力電子 Industrial Technology '
                +'R&amp;D Master Program on Power Electronics'),
               ('SCI', 'SCI 　理學院學士班 '
                +'Interdisciplinary Program of Sciences'),
               ('SLS', 'SLS 　先進光源科技學位學程 Doctor Program of Science '
                +'and Technology of Synchrotron Light Source'),
               ('SNHC', 'SNHC　社群人智國際學程 Social Networks and '
                +'Human-Centered Computing'),
               ('SOC', 'SOC 　社會所 Sociology'),
               ('STAT', 'STAT　統計所 Statistics'),
               ('STAU', 'STAU　統計所與交大合作課程 Statistics &amp; NCTU'),
               ('TE', 'TE  　師培中心(中等教程) Teacher Education'),
               ('TEG', 'TEG 　師培中心(一般課程) Teacher Education '
                +'(General Courses)'),
               ('TEX', 'TEX 　師培中心與竹教大合作 '
                +'Teacher Education and National Hsinchu University '
                +'of Education'),
               ('TIGP', 'TIGP　國際研究生學程 Taiwan International '
                +'Graduate Program'),
               ('TL', 'TL  　台文所 Taiwan Literature'),
               ('TM', 'TM  　科管所 Technology Management'),
               ('UPMT', 'UPMT　科管院學士班 Double Specialty '
                +'Program of Management and Technology'),
               ('W', 'W   　W課號課程 Interschool Courses'),
               ('WH', 'WH  　台聯大及互惠課程'),
               ('WW', 'WW  　交大課程 NCTU COURSE'),
               ('WZ', 'WZ  　外校課程'),
               ('X', 'X   　X抵免課程'),
               ('XA', 'XA  　抵免課程(大)'),
               ('XZ', 'XZ  　抵免課程(研)'),
               ('YZ', 'YZ  　課務組專用'),
               ('ZY', 'ZY  　服務學習 Service Learning'),
               ('ZZ', 'ZZ  　勞作服務 Student Service'),)

GEC_CHOICE = (('', '---'),
              ('Core GE courses 1', '核心通識向度一'),
              ('Core GE courses 2', '核心通識向度二'),
              ('Core GE courses 3', '核心通識向度三'),
              ('Core GE courses 4', '核心通識向度四'),
              ('Core GE courses 5', '核心通識向度五'),
              ('Core GE courses 6', '核心通識向度六'),
              ('Core GE courses 7', '核心通識向度七'),)

GE_CHOICE = (('', '---'),
             ('Natural Sciences', '自然科學領域'),
             ('Social Sciences', '社會科學領域 '),
             ('Humanities', '人文學領域'),)
