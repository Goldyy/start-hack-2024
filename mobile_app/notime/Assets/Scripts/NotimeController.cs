using UnityEngine;

/// <summary>
/// Controls camera movement and zoom based on mouse and touch input.
/// Allows for panning the camera with a single touch or mouse drag, and zooming with a pinch gesture or mouse wheel.
/// </summary>
public class NotimeController : MonoBehaviour
{
    /// <summary>
    /// The speed at which the camera moves across the scene.
    /// </summary>
    public float moveSpeed = 0.05f;

    /// <summary>
    /// The speed at which the camera zooms in or out.
    /// </summary>
    public float zoomSpeed = 0.1f;

    private Vector2 previousPosition;
    private bool isZooming = false;

    void Update()
    {
        // Handle mouse input for camera movement.
        if (Input.GetMouseButtonDown(0))
        {
            previousPosition = Input.mousePosition;
        }
        else if (Input.GetMouseButton(0) && Input.touchCount < 2) // Prevent camera movement when zooming with two fingers.
        {
            Vector2 deltaPosition = (Vector2)Input.mousePosition - previousPosition;
            MoveCamera(deltaPosition);
            previousPosition = Input.mousePosition;
        }

        // Handle touch input for camera movement.
        if (Input.touchCount == 1 && !isZooming)
        {
            Touch touch = Input.GetTouch(0);

            if (touch.phase == TouchPhase.Moved)
            {
                Vector2 deltaPosition = touch.deltaPosition;
                MoveCamera(deltaPosition);
            }
        }
        // Handle touch input for zooming.
        else if (Input.touchCount == 2)
        {
            // Perform zoom using two fingers.
            Touch touchOne = Input.GetTouch(0);
            Touch touchTwo = Input.GetTouch(1);

            Vector2 touchOnePrevPos = touchOne.position - touchOne.deltaPosition;
            Vector2 touchTwoPrevPos = touchTwo.position - touchTwo.deltaPosition;

            float prevTouchDeltaMag = (touchOnePrevPos - touchTwoPrevPos).magnitude;
            float touchDeltaMag = (touchOne.position - touchTwo.position).magnitude;

            float deltaMagnitudeDiff = prevTouchDeltaMag - touchDeltaMag;

            ZoomCamera(deltaMagnitudeDiff * zoomSpeed);
            isZooming = true;
        }
        else
        {
            isZooming = false;
        }
    }

    /// <summary>
    /// Moves the camera based on input delta position.
    /// Translates the camera in the opposite direction of the drag to simulate moving the environment.
    /// </summary>
    /// <param name="deltaPosition">The change in position since the last frame, used to calculate direction and distance of camera movement.</param>
    void MoveCamera(Vector2 deltaPosition)
    {
        Vector3 direction = new Vector3(-deltaPosition.x * moveSpeed, 0, -deltaPosition.y * moveSpeed);
        transform.Translate(direction, Space.World);
    }

    /// <summary>
    /// Zooms the camera in or out based on the input increment.
    /// </summary>
    /// <param name="increment">The amount to zoom by, determined by the change in distance between two touch points.</param>
    void ZoomCamera(float increment)
    {
        transform.Translate(0, 0, increment, Space.Self);
    }
}


