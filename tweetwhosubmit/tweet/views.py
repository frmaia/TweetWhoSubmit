# Create your views here.
from models import CadastroUsuario
from tweetwhosubmit.tweet.forms import CadastroUsuarioForm 
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
import settings


@csrf_exempt
def listagem(request):
    
    cadastrados = CadastroUsuario.objects.all()
    return render_to_response('listagem.html', {'cadastrados' : cadastrados} )


@csrf_exempt
def adicionar_cadastro(request):
    if request.method == "POST":
        form = CadastroUsuarioForm(request.POST)
            
        if not form.is_valid():            
            render = render_to_response('cadastro.html', {'form': form })

        else:
            form.save()
            
            if form.instance.conta_twitter:
                info = form.instance.conta_twitter
            else:
                info = form.instance.nome
                
            this_url = request.build_absolute_uri(reverse('listagem'))
            
            twitter_msg = u"'%s' acabou de se cadastrar no site %s ." % (info, this_url)
            twitter_posted = _postToTwitter(twitter_msg)
            
            d = {
                 'twitter_posted' : twitter_posted, 
                 'twitter_msg' :twitter_msg,
                 'twitter_url_profile' : settings.TWITTER_CONFIGS['public_profile_url']
                 }
            
            render = render_to_response('confirmacao_cadastro.html', d)
        
    else:
        render = render_to_response('cadastro.html', {'form': CadastroUsuarioForm()} )
    
    return render


def _postToTwitter(twitter_msg):       
    try:
        import twitter
        api = twitter.Api(
                  consumer_key = settings.TWITTER_CONFIGS['consumer_key'],
                  consumer_secret = settings.TWITTER_CONFIGS['consumer_secret'],
                  access_token_key = settings.TWITTER_CONFIGS['access_token_key'],
                  access_token_secret = settings.TWITTER_CONFIGS['access_token_secret'],
                  )
        api.PostUpdate(twitter_msg)
        return True
    except:
        return False
