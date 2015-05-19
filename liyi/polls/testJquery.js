  <script type="text/javascript">
  $(document).ready(function(){
      $("#lForm").submit(function(){
        val = $('#send')[0].value;
        $.ajax({
          type:"get",
          url:"/search_result/",
          data: {'val':val},
          dataType:"html",
          success: function(msg){
            alert(msg);
            if(msg != null)
            {
              alert("suc:"+ msg);
              window.location.href = "/search_form/";
            }
           }
          })
        })
      })
  </script>