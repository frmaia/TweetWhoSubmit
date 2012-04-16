from django.forms import ModelForm
from tweetwhosubmit.tweet.models import CadastroUsuario


class CadastroUsuarioForm(ModelForm):
    class Meta:
        model = CadastroUsuario
        
        