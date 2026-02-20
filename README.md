A FastAPI application that processes user-submitted prompts through an HTML form, utilizes Gemini to generate diagram elements, and renders the result in an Excalidraw canvas.

The prompt must include types of diagram:

1. sequence
2. flowchart
3. architecture
4. erd
5. class
6. state
7. mindmap
8. swimlane
9. network
10. timeline
11. gitflow
12. c4


For example,

```txt
draw a sequence diagram of booking system
```

the prompt above include `sequence` 

# Run on Linux

```python
fastapi dev main.py
```
