var count=1;
var coordinate='';

var n;
var min=0;
var flag=0;
var csrftoken='';
function deleteTime(divNum) {
	event.preventDefault();
	$('#'+divNum).remove();
	min++;
	if(flag<4)
  		$("#confirm_date").removeAttr('disabled');
}

function setTime() {
	event.preventDefault();
	var content=$('#selector').val();
	var divIdName;
 	divIdName="my"+count+"Div";  
 	
  	$('#timeContent').append(' <div id='+divIdName+'>'+content+'<a href="#" onclick="deleteTime(\'' + divIdName + '\')">   Delete</a></div>');
  	count++;
  	var flag=count-min;
  	if(flag==4)
  		$("#confirm_date").attr("disabled", "disabled");
  	
}
var chosenList=new Array(3);
function saveVote(){
  var i=0;
  while (i<3){
    var radioName="radio"+i+"Name";
    //alert(radioName);
    if($("#"+radioName).length>0){
      var radioObj = document.getElementById(radioName);
      if(radioObj.checked){
        chosenList[i]=1;
      }
      else{
        chosenList[i]=0;
      }
    }else
      chosenList[i]=0;
    i++;
  }  
}
var today='';
function submitComment(){
  event.preventDefault();
	var comment=$('#commentContent').val();
  var userName=$('#userName').val();
  var commentTimeArray=today.split("T");
  var commentTime=commentTimeArray[0]+" "+commentTimeArray[1];
  
  if($('#commentContent').val()=="")
    $("#wrong").css('display', 'block');
  else{
    $('#commentTable').prepend('<tr><td><span style="color:blue">'+userName+'</span>: '+
			htmlEscape(comment)+' </td><td>'+commentTime+'</td></tr>');
    $('#commentContent').val('');
	  //$('#commentTable tr:first').after('<tr></tr>');
    $.ajax({
      url:'/comments/add',
      type:'POST',
      data:{
        comment:comment,
        eventid:$("#eventId").val(),
        csrftoken:csrftoken,
      }
    });
  }
} 
//window.location.reload();
function joinEvent(){
  saveVote();
  var firstVote=chosenList[0];
  var secVote=chosenList[1];
  var thirdVote=chosenList[2];
  //$('#joinAlert').modal('show');
  if((firstVote==0)&&(secVote==0)&&(thirdVote==0))
    $('#joinAlert').modal('show');
    //alert("Please make votes of the time before you join!");
  //alert(chosenList);
  else{
  $.ajax({
    		url: "/event/submitvote", 
 				type: "POST",
 				data: {
          firstVote:firstVote,
          secVote:secVote,
          thirdVote:thirdVote,
          eventid:$("#eventId").val(),
          csrftoken:csrftoken,
        }
      });
  //jConfirm('Successfully join this event!', 'Confirmation Dialog', function() {
  //window.location.href="/home"; 
  //});
  //jAlert('Successfully join this event!');
  //bootbox.alert("Successfully join this event!");
  //$('#dialog-message').modal('toggle'); 
  //myalert("Test", "This is a test modal dialog");
  //alert("Join this event successfully!");
  $('#joinModal').modal('show');
  $("#join").attr("disabled", "disabled");
  //$('#joinModal').modal('toggle');
  //alert(chosenList);
  }
}
$(document).ready(function() {
  csrftoken=$('#csrftoken').val();
  var date = new Date;
  //date.setTime(result_from_Date_getTime);
  var seconds = date.getSeconds();
  var minutes = date.getMinutes();
  var hour = date.getHours();
  var year = date.getFullYear();
  var month = date.getMonth()+1; // beware: January = 0; February = 1, etc.
  var day = date.getDate();
  month="0" + month;
  if(minutes<10)
    minutes="0"+minutes;
  if(hour<10)
    hour="0"+hour;
  today = year+"-"+month+"-"+day+"T"+hour+":"+minutes;
  
	$('#selector').val(today);
        google.maps.event.addDomListener(window, 'load', initialize);
        //$('#submitEvent').click(submitForm);
	
});
