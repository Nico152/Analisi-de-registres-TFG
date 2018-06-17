
function myFunction(nom_llibre,num_registre){
	//alert(nom_llibre);
	nom_llibre = nom_llibre.replace('/','*')
	window.location.assign('http://localhost:8000/tfg/'+nom_llibre+'/'+num_registre);
	//alert(window.location.pathname);
}