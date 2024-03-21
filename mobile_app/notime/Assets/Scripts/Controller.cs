using System;
using UnityEngine;

public class Controller : MonoBehaviour
{

    /// <summary>
    /// An array of GameObjects representing the steps in a process or sequence within the game.
    /// </summary>
    public GameObject[] steps;

    /// <summary>
    /// The GameObject used as a pointer to indicate a specific location, typically for selection or navigation purposes.
    /// </summary>
    public GameObject locationPointer;

    /// <summary>
    /// The parent Transform under which dynamically instantiated objects like location pointers are organized.
    /// </summary>
    public Transform storeParent;

    /// <summary>
    /// A reference Transform used as a null or origin point in the store, from which relative positions can be calculated.
    /// </summary>
    public Transform storeNullPointer;

    /// <summary>
    /// The current location of the human or player character within the game environment.
    /// </summary>
    public Transform humanCurrentLocation;

    /// <summary>
    /// The container holding waypoints for navigation or movement paths in the scene.
    /// </summary>
    public Transform wayPointsContainer;

    /// <summary>
    /// A Transform representing the direction or target the arrow points towards.
    /// </summary>
    public Transform arrow;

    /// <summary>
    /// The main camera GameObject used for the primary viewpoint in the scene.
    /// </summary>
    public GameObject mainCamera;

    /// <summary>
    /// The camera used specifically in the third step of the process or sequence.
    /// </summary>
    public Transform xrCameraStep3;

    /// <summary>
    /// The camera used specifically in the second step of the process or sequence.
    /// </summary>
    public Transform xrCameraStep2;

    /// <summary>
    /// A GameObject representing a red cube used specifically in the third step of the process or sequence.
    /// </summary>
    public Transform redCubeStep3;


    /// <summary>
    /// Called on the frame when a script is enabled just before any of the Update methods are called the first time.
    /// It's used here to perform initial setup by selecting a default product, in this case, "Milk".
    /// </summary>
    void Start()
    {
        Select_product("Milk");
    }



    /// <summary>
    /// Called every frame, used to update game logic and frame-dependent behaviors.
    /// In this implementation, it retrieves the current position (X,Y) from a Cisco device for a human target and updates the rotation of an arrow object.
    /// The arrow's rotation is synchronized with the Y-axis rotation of a camera, referenced as 'xrCameraStep2', while maintaining its original rotations on the X and Z axes.
    /// </summary>
    void Update()
    {
        GetXYFromCiscoForHuman();
        arrow.eulerAngles = new Vector3(arrow.eulerAngles.x, xrCameraStep2.eulerAngles.y, arrow.eulerAngles.z);
    }



    /// <summary>
    /// Activates a specific step in a sequence based on the provided step number, and deactivates all others.
    /// This method logs the activation event and iterates through an array of step objects, activating only the specified step (zero-based index adjusted by subtracting 1 from the step number) and deactivating all other steps.
    /// </summary>
    /// <param name="stepNumber">The step number to activate. Note: This is expected to be 1-indexed.</param>
    public void ActivateStep(int stepNumber)
    {
        Debug.Log("Activate Step " + stepNumber);
        for(int i = 0; i< steps.Length; i++)
        {
            if(i == stepNumber - 1)
            {
                steps[i].SetActive(true);
            }
            else
            {
                steps[i].SetActive(false);
            }
        }
    }



    private bool movementOn = true;
    /// <summary>
    /// Toggles the movement state of an object or character.
    /// If movement is currently enabled, this method disables it, and vice versa.
    /// This is useful for enabling or disabling movement based on certain conditions or inputs.
    /// </summary>
    public void InvertMovement()
    {
        if (movementOn)
        {
            movementOn = false;
        }
        else
        {
            movementOn = true;
        }
    }



    /// <summary>
    /// Spawns a red cube at a position slightly in front of the 'xrCameraStep3' object.
    /// The spawn position is determined by offsetting the camera's current position forward by a small amount (0.01 units).
    /// This method is useful for visualizing or interacting with elements in 3D space relative to the camera's position.
    /// </summary>
    public void SetCubeStep3()
    {
        Vector3 SpawnPosition = xrCameraStep3.transform.forward * 0.01f + xrCameraStep3.transform.position;
        Instantiate(redCubeStep3, SpawnPosition, Quaternion.identity);
    }



    /// <summary>
    /// Retrieves the X and Y coordinates for a specified product from a Cisco system or device.
    /// This method logs the request for coordinates with the specified product name and returns a hardcoded set of coordinates as an example.
    /// It's designed to simulate the process of querying a Cisco device or system for spatial data related to a product's location.
    /// </summary>
    /// <param name="product_name">The name of the product for which the coordinates are requested.</param>
    /// <returns>A Vector2 containing the X and Y coordinates of the specified product.</returns>
    private Vector2 GetXYFromCiscoForProduct(string product_name)
    {
        Debug.Log("Get Coordinates from Cisco for Product " + product_name);        
        return new Vector2(4.3f, 21.52f);
    }



    private int countWayPoints = 0;
    private float timePassed = 0;
    public float speedOfHuman = 0.1f;
    /// <summary>
    /// Updates the current location of a human target based on waypoints, if movement is enabled.
    /// This method checks if movement is allowed and periodically updates the human's position towards the next waypoint.
    /// It will skip the update if not enough time has passed based on the 'speedOfHuman'.
    /// Upon reaching a waypoint, it advances to the next one. If the last waypoint is reached, it activates a specific step and potentially disables the main camera.
    /// Note: This method involves mocked behavior for demonstration and may reference external state such as 'movementOn', 'timePassed', and 'speedOfHuman'.
    /// </summary>
    private void GetXYFromCiscoForHuman()
    {
        // pause the movement
        if (!movementOn) return;

        // implement slow movement of human point
        timePassed += Time.deltaTime;
        if (timePassed < speedOfHuman)
        {            
            return;
        }
        else
        {
            timePassed = 0f;
        }        

        // Select or update current wayPoint
        if (Math.Abs(humanCurrentLocation.position.x - wayPointsContainer.GetChild(countWayPoints).position.x) < 0.1 &&
            Math.Abs(humanCurrentLocation.position.z - wayPointsContainer.GetChild(countWayPoints).position.z) < 0.1)
        {            
            countWayPoints += 1;
            if(countWayPoints > wayPointsContainer.childCount - 1)
            {
                // blind human arrived target.
                ActivateStep(3);
                mainCamera.gameObject.SetActive(false);
                return;
            }
        }
        
        // Calculate new Coordintes for human based by waypoints
        float x;
        if (Math.Abs(humanCurrentLocation.position.x - wayPointsContainer.GetChild(countWayPoints).position.x) < 0.1)
        {            
            x = humanCurrentLocation.position.x;
        }
        else if (humanCurrentLocation.position.x < wayPointsContainer.GetChild(countWayPoints).position.x)
        {
            x = humanCurrentLocation.position.x + 0.01f;
        }
        else
        {
            x = humanCurrentLocation.position.x - 0.01f;
        }


        float z;
        if (Math.Abs(humanCurrentLocation.position.z - wayPointsContainer.GetChild(countWayPoints).position.z) < 0.1)
        {            
            z = humanCurrentLocation.position.z;
        }
        else if (humanCurrentLocation.position.z < wayPointsContainer.GetChild(countWayPoints).position.z)
        {
            z = humanCurrentLocation.position.z + 0.01f;
        }
        else
        {
            z = humanCurrentLocation.position.z - 0.01f;
        }

        
        // update position of human point and arrow
        humanCurrentLocation.position = new Vector3(x, humanCurrentLocation.position.y, z);
        arrow.position = new Vector3(x, humanCurrentLocation.position.y, z);
    }

    /// <summary>
    /// Selects a product by name and positions a location pointer at the product's location within the store.
    /// This method simulates a backend call to retrieve the X and Y coordinates of the specified product, likely from a database or an external service like a Cisco application.
    /// A new location pointer GameObject is instantiated and positioned based on the retrieved coordinates relative to a predefined null pointer in the store, adjusting for store layout and elevation.
    /// </summary>
    /// <param name="product_name">The name of the product to locate. This name is used to query the product's coordinates.</param>
    public void Select_product(string product_name)
    {
        // simulate REST agains Backend (Cisco-App)
        Vector2 xy = GetXYFromCiscoForProduct(product_name);

        //Set location pointer for target product
        GameObject locationPointerTargetProduct = Instantiate(locationPointer, storeParent);
        float x = storeNullPointer.position.x - xy.x;
        float y = storeNullPointer.position.y + 1;
        float z = storeNullPointer.position.z - xy.y;
        locationPointerTargetProduct.transform.position = new Vector3(x,y,z);
    }

    
}
