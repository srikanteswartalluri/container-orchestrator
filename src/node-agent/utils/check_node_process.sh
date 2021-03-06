for i in {12375..12379}
do
echo "$i" && docker exec co_node_$i ps -ef | grep Node
done
