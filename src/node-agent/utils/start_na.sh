for i in {12375..12378}
do
echo "$i" && docker exec co_node_$i python3 /NodeAgent.py -n co_node_$i -p &
done
for i in {12375..12378}
do
echo "$i" && docker exec co_node_$i python3 /NodeAgent.py -n co_node_$i -c &
done