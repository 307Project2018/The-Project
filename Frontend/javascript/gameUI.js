window.onload = function(){
	window.globalVar = true;
};

function displayID(id){
	var cavas = document.getElementById("textBox");
	cavas.innerHTML = id;
}

function makeIdAppear(id){
	var cavas = document.getElementById("textBox");
	cavas.innerHTML = id;
}