window.onload = function(){
	function makeCollection(){
		var grid = document.getElementById("collectionGrid");
		for(var i = 0; i < 24;i++){
			var cell = document.createElement("div");
			cell.className = "square";
			cell.innerText = i;
			grid.appendChild(cell);
		}
	}
	makeCollection();
};
