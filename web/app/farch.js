queue()
    .defer(d3.json, "./data_by_year.json")
    .defer(d3.json, "./when_it_be_over.json")
    .await(ready);
console.log("hey");
function ready(error, data, over) {
    console.log(error, data, over);
}
