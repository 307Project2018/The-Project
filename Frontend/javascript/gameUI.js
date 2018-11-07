window.onload = function(){
	window.globalVar = true;
};

function displayID(id){
	alert(id);
}

function makeIdAppear(id){
	document.getElementById("textBox").innerHTML = id;
}