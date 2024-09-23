from django.shortcuts import render
from .form import ImageUploadForm
from .models import ImageData
from PIL import Image
import pytesseract
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.probability import FreqDist
from django.shortcuts import render




def home(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.cleaned_data['image']
            img_obj = Image.open(img)  
            img_obj = img_obj.convert('L')
            text = pytesseract.image_to_string(img_obj)
            imagedata = ImageData(image=img) 
            imagedata.save() 
            return render(request, 'index.html', {'text': text, 'image': imagedata})
    else:
        form = ImageUploadForm()
 
    imagedata= ImageData.objects.all()
    context = {'form': form, 'imagedata': imagedata}
    return render(request, 'index.html', context)

def analyze_summary(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        
        # Tokenize the text into sentences
        sentences = sent_tokenize(text)
        
        # Remove stopwords and stem the words
        stop_words = set(stopwords.words("english"))
        ps = PorterStemmer()
        word_tokens = nltk.word_tokenize(text.lower())
        filtered_tokens = [ps.stem(w) for w in word_tokens if w.isalnum() and not w in stop_words]
        
        # Calculate word frequency distribution
        fdist = FreqDist(filtered_tokens)
        
        # Get the most frequent words
        most_frequent_words = fdist.most_common(5)
        
        # Generate the summary by joining the most frequent words
        summary = " ".join([word for word, _ in most_frequent_words])
        
        return render(request, 'summary.html', {'summary': summary})
    else:
        return render(request, 'analyze.html')

