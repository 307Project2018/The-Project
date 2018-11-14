window.onload = function(){
	function createBoard(){
		
		var board = document.getElementById("boardGrid");
		
		for(var y = 7; y>-1;y--){
			for(var x = 0; x<8;x++){
				var square = document.createElement("div");
				square.className = "boardSquareB";
				square.setAttribute("onclick","displayID(this.id)");
				square.setAttribute("onmouseover","makeIdAppear(this.id)");
				square.id = x.toString()+y.toString();
				board.appendChild(square);
			}
		}
		
	}
	createBoard();
};

function displayID(id){
	alert(id);
}

function makeIdAppear(id){
	document.getElementById("textBox").innerHTML = id;
}