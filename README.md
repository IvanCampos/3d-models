# 3d-models
Collection of 3D models generated with AI using the Blender Python API


  
## Adding a model within a visionOS RealityView
```
if let entity = try? await ModelEntity(named: "name_of_3d_model") {
    entity.position = [0, 1.5, -1]
    entity.scale = [0.1, 0.1, 0.1]
    entity.components.set(InputTargetComponent())
    entity.generateCollisionShapes(recursive: false)
    var material = PhysicallyBasedMaterial()
    material.baseColor = .init(tint: .green, texture: nil)
    entity.model?.materials = [material]
    content.add(entity)
}
```

### What the Code Does
1. Asynchronous Loading:
* The code uses try? await ModelEntity(named: "name_of_3d_model") to load the model asynchronously. This is good if you’re working in an async context, but note that using try? will silently ignore any errors if the model fails to load.  

2. Setting Position and Scale:
* The model’s position is set to [0, 1.5, -1] and its scale to [0.1, 0.1, 0.1]. This positions the model in the scene and scales it appropriately. Ensure these values match the desired scene layout and model size.  

3. Input and Collision Setup:  
* The code adds an InputTargetComponent to the entity. This facilitates user interactions (e.g., taps or gestures).
* It calls entity.generateCollisionShapes(recursive: false), which is important for enabling collision detection. This is especially useful if you plan to interact with the model in AR/VR environments.

4. Material Customization:  
* A new PhysicallyBasedMaterial is instantiated.  
* The baseColor is set using a tint (green) without a texture. This changes the appearance of the model by overriding its default materials.
* The material is then applied by setting entity.model?.materials to an array containing your custom material.

5. Adding to the Scene:  
* Finally, the entity is added to content, which represents your scene’s content container.  
