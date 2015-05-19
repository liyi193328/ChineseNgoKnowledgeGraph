
var nameNGO,rt;
d3.json("/static/data/ngoName.json",function(error,root){
  if(error)
    return console.error(error);
    rt = root;
    nameNGO = root.nameAll;
    compelete();
  });

$("#Sbut").click(function(){
    // alert("click");
    sendData();
});
