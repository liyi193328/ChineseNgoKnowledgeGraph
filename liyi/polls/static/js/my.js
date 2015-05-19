
//autocompelete
function compelete() {
  orgType = ["国内机构","境外机构","基金会","企业","政府部门"];
    $("#orgType").autocomplete({
        source: orgType,
        minLength: 0
    }).focus(function(){            
       $(this).autocomplete('search', $(this).val())
     });
  var field = ['劳工', '环保与动保', '三农/社区发展与救灾', '教育', '健康与防艾', 
                '性别与性少数', '老人与儿童', '残障', '社会创新/社会企业', 
                '能力建设/研究/支持/咨询', '民族/宗教/文化/艺术', '生物多样性',
                '企业社会责任', '社工','慈善事业','社会创新/社会企业','其他','能源','气候变化','反腐败和透明化'];
    $("#field").autocomplete({
        source: field,
        minLength: 0
    }).focus(function(){            
       $(this).autocomplete('search', $(this).val())
     });
  var province = ['北京市', '上海市', '天津市', '重庆市', '黑龙江省', 
  '吉林省', '辽宁省', '内蒙古省', '新疆省', '甘肃省', '宁夏省', '山西省',
   '陕西省', '河南省', '河北省', '山东省', '西藏省', '四川省', '青海省', '湖南省', 
   '湖北省', '江西省', '安徽省', '江苏省', '浙江省', '福建省', '云南省', '贵州省', '广西省', 
   '广东省', '海南省', '香港特别行政区', '台湾', '澳门特别行政区'];
    $("#province").autocomplete({
        source: province,
        minLength: 0,
        // maxLength:
    }).focus(function(){            
       $(this).autocomplete('search', $(this).val())
     });

    $("#nameA").autocomplete({
        source: nameNGO,
        minLength: 0
    }).focus(function(){            
       $(this).autocomplete('search', $(this).val())
     });
    $("#nameB").autocomplete({
        source: nameNGO,
        minLength: 0
    }).focus(function(){            
       $(this).autocomplete('search', $(this).val())
     });
}


//showData
function showData(data){
  // text = JSON.stringify(data['nodes'])
  // alert(text)
  console.log(data.nodes.length);
  console.log(data);
  console.log(data.nodes);
  // for(var i = 0; i<data.length; i++){

  // }
}
//get search word
function sendData() {
  var flag = false;
  orgType = $("#orgType").val();
  field = $("#field").val();
  province = $("#province").val();
  nameA = $("#nameA").val();
  nameB = $("#nameB").val();
  if(nameB != null && nameA == null){alert("请输入A机构的名字以便于寻找关系!");return;}
  if (orgType != null || field != null || province != null || nameA != null || nameB != null) flag = true;
  if (flag) { // search
    // alert("searching:"+orgType+"\n"+field+"\n"+province+"\n"+nameA+"\n"+nameB)
    $.ajax({
      type: "get",
      url: "/getSearchData/",
      data: {
        "orgType": orgType,
        "field": field,
        "province": province,
        "nameA": nameA,
        "nameB":nameB
      },
      dataType: "json",
      success: function(data) { // data is json,include nodes,edges,property
        // showData(data);
        // render(data);
        var svgId = "#graph";
        render(data,svgId);
      }
    });
  }
}