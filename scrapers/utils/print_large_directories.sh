python ./scrapers/utils/remove_non_python.py
for i in ./scrapers/data/raw_repos/*; 
    do 
    count=$(find $i |wc -l); 
    if [ $count -gt 100 ]
    then
        echo $i; 
        echo $count
        rm -rf $i
    fi
done;