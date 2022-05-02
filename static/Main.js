
const tbDivWidth = document.getElementById('tba').offsetWidth //width of table div


function showContents(file, json_){
      console.log(tbDivWidth)
      const tb = document.getElementById('fileTable'); //gets table from html
      var id = parseInt(file[11]); //grabs only the row number from the id
      var jFile = json_.Contents[id];  
      if(jFile.Type == 'directory'){
            for(var j=0; j<tb.rows.length; j++){
                  if(tb.rows[j].cells.length > 1){
                        tb.rows[j].cells[1].innerHTML = '';
                  }
            } 
            for(var k=0; k<jFile.Contents.length; k++){
                  if( k<tb.rows.length){
                        var row = tb.rows[k];
                        var cell = row.insertCell(1)
                        cell.innerHTML = jFile.Contents[k].Name
                  }else{
                        var row = tb.insertRow(1)
                        var cell = tb.insertCell(1)
                        cell.innerHTML = jFile.contents[k].Name
                  }
            }
      }
}



function getData(id_){ //this function gets the data for the selected project 

      var projTitle  = document.getElementById('projName' + id_).innerText; //grabs the name of a selected project
      var url = 'http://127.0.0.1:5000/get_data/' + lang + '/' + projTitle + '/' + id_; //request corresponding data from the backend
      var eventArray = [];
      var projID;
      const tb = document.getElementById('fileTable'); //table containing files  of selected project
      const title = document.getElementById('selProjTitle'); //grabs title section of reslts div
      tb.innerHTML = ""; //clears table before inserting new values


      fetch(url) //fetch request
      .then(res => res.json())
      .then(json => {
            title.innerHTML = json.Name; //displays the title of the current file
            projID = json.id; //grabs the id 
            for(var row = 0; row<json.Contents.length; row++){ //create nw row for each file
                  var newRow = tb.insertRow(row); //create new row
                  var cell = newRow.insertCell(0); //insert cell into new row

                  cell.innerHTML = json.Contents[row].Name; //display file name in table
                  cell.id = 'projectFile' + row; //set unique id of each cell
                  eventArray[row]  = cell.id ; //add the cell id to the eventArray. This will be used to detect clicks on each row
            }

            for( var i=0; i<eventArray.length; i++){ //this loop detects which row has been clicked on
                  var currentRow = eventArray[i]; //gets id for current row
                  var createClickHandler = function(row){ //callback function to handle onclicks
                        return function() {
                              var cell = document.getElementById(row); //calls the selected cell
                              cell.width = tbDivWidth/3; //set width of cell
                              for(var j=0; j<eventArray.length; j++){ 
                                    document.getElementById(eventArray[j]).style = 'background-color: black; color:chartreuse;'
                              } //color all cells black with green text
                              cell.style = 'background-color:cyan; color: black;'; //make selected cell cyan with black text

                              showContents(row,json);
                        };
                  };
                  document.getElementById(currentRow).onclick = createClickHandler(currentRow);
            }
            
      });
}


function refresh(language){
      console.log(language);
}