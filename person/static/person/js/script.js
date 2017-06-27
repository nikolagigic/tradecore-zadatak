function check(){
            name=document.forms["register"]["name"].value;
            surname=document.forms["register"]["surname"].value;
            email=document.forms["register"]["email"].value;
            username=document.forms["register"]["username"].value;
            password=document.forms["register"]["password"].value;

            if (name==null || surname==null || email==null || username==null || password==null){
                alert("Please provide all asked information.");
                return false;
            }
        }