window.onload = function(){
	function makeCollection(){
		var grid = document.getElementById("collectionGrid");
		for(var i = 0; i < 24;i++){
			var cell = document.createElement("div");
			cell.className = "square";
			cell.innerText = i;
			cell.id = "cell" + i;
			//cell.src = 'C:\\Users\\Patrick\\Desktop\\pawn.jpg'
			cell.setAttribute("onclick","changeUI(this.id)");
			grid.appendChild(cell);
		}
	}
	makeCollection();
};

function changeUI(id){
	document.getElementById("nameField").innerHTML = id;
	document.getElementById("pictureField").innerHTML = id;
	document.getElementById("movesetField").innerHTML = id;
	document.getElementById("hpattField").innerHTML = id;
}