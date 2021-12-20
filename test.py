# test/scrap file for doing short tests or debugs

def println(str):
    print(str + "\n")

src = [
    'APS Pharmacological Targets in Health and Disease: â€œWhat is drugable?â€\x9d',
    'National Association of Women Lawyers â€œNAWLâ€\x9d 2021 Mid-Year Conference Scott'
    ]


try:
    for row in src:
        ss = row
        #println ("Raw: " + ss)
        ss = str(ss.encode(encoding="ascii", errors="backslashreplace"))
        print("backslashreplace: " + str(ss))
        ss = row
        ss = str(ss.encode(encoding="ascii", errors="replace"))
        print("replace: " + str(ss))
        ss = row
        ss = str(ss.encode(encoding="ascii", errors="ignore"))
        print("ignore: " + str(ss))
        ss = row
        ss = str(ss.encode(encoding="ascii", errors="namereplace"))
        print("namereplace: " + str(ss))        
        ss = row
        ss = str(ss.encode(encoding="ascii", errors="xmlcharrefreplace"))
        print("xmlcharrefreplace: " + str(ss))        
except Exception as e:
    println(str(e))

ii = 1





