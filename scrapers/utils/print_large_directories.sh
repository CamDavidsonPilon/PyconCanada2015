for i in /root/PyconCanada2015/scrapers/data/raw_repos/*; 
    do 
    count=$(find $i |wc -l); 
    if [ $count -gt 3000 ]
    then
        echo $i; 
        echo $count
    fi
done;