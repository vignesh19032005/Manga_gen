from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .ai_services import MangaAIService

def index(request):
    return render(request, 'manga_app/index.html')

def panels(request):
    """Render the panels page"""
    return render(request, 'manga_app/panels.html')

def gallery(request):
    return render(request, 'manga_app/gallery.html')

def about(request):
    return render(request, 'manga_app/about.html')

@csrf_exempt
def generate_manga(request):
    """Generate manga story and scenes"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    
    try:
        # Parse JSON data
        data = json.loads(request.body)
        
        # Extract parameters
        genre = data.get('genre', '')
        length = data.get('length', '')
        audience = data.get('audience', '')
        premise = data.get('premise', '')
        elements = data.get('elements', [])
        
        # Validate required fields
        if not all([genre, length, audience, premise]):
            return JsonResponse({
                'success': False,
                'error': 'Please fill in all required fields'
            }, status=400)
        
        # Initialize AI service
        ai_service = MangaAIService()
        
        # Generate story
        story_result = ai_service.generate_story(genre, length, audience, premise, elements)
        
        if story_result['success']:
            # Extract scenes
            scenes_result = ai_service.extract_key_scenes(story_result['story'])
            
            if scenes_result['success']:
                return JsonResponse({
                    'success': True,
                    'story': story_result['story'],
                    'scenes': scenes_result['scenes']
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': scenes_result['error']
                }, status=500)
        else:
            return JsonResponse({
                'success': False,
                'error': story_result['error']
            }, status=500)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
def generate_panels(request):
    """Generate manga panels for a story"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        scenes = data.get('scenes', [])
        art_style = data.get('art_style', 'modern manga')
        
        if not scenes:
            return JsonResponse({
                'error': 'No scenes provided'
            }, status=400)
            
        ai_service = MangaAIService()
        panels = []
        
        for scene in scenes:
            result = ai_service.generate_panels(scene, art_style)
            if result['success']:
                panels.append({
                    'scene': scene,
                    'image_url': result.get('image_url'),
                    'message': result.get('message')
                })
            else:
                return JsonResponse({
                    'error': f"Failed to generate panel: {result.get('error')}"
                }, status=500)
        
        return JsonResponse({
            'success': True,
            'panels': panels
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
