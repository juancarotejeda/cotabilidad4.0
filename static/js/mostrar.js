    function mostrar(){
    if  (document.getElementById('autorizacion').style.display == 'block')
    {document.getElementById('autorizacion').style.display = 'none';
    document.getElementById('desautorizacion').style.display = 'block';}
    else
    {document.getElementById('autorizacion').style.display = 'block';
    document.getElementById('desautorizacion').style.display = 'none';}
    }
    
    var testear=document.getElementById("pagos").innerHTML;
    alert(testear);