d=open('date_index.txt','w')
year = 1960
day = 1
main_count = 0
while year < 2100:
    if year%400 == 0:
        count=1
        while count < 367:
            if count != 60:
                d.write(str(day)+' ')
                main_count+=1
            count+=1
            day+=1
    elif year%100 == 1:
        count=1
        while count <366:
            d.write(str(day)+' ')
            count+=1
            day+=1
            main_count+=1
    elif year%4 == 1:
        count=1
        while count < 367:
            if count != 60:
                d.write(str(day)+' ')
                main_count+=1
            count+=1
            day+=1
    else:
        count=1
        while count < 366:
            d.write(str(day)+' ')
            count+=1
            day+=1
            main_count+=1
    year+=1
    print year 
   
d.close()