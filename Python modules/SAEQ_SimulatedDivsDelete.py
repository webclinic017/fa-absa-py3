import ael, string
    

strm = ael.DividendStream.select()

for st in strm.members():
    #print m.name
    
    #if (string.find(st.name,'1') != -1):
        #print st.name
        #print m.estimates()
        #print st.annual_growth,st.div_per_year
        st = st.clone()
        for est in st.estimates():
            if est.description == 'Simulated':
                
              est.delete()
        st.commit()
