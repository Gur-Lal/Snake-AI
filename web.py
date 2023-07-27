import pygame,sys,random,time, gradio as gr
from pygame.math import Vector2

#def greet(name):
#    return "Hello " + name + "!"

def user_inputs(inputs):
    return "Hello " + inputs + "!"

demo = gr.Interface(fn=user_inputs, inputs="w", outputs="text")
    
demo.launch()  