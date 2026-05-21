
import json
import os
import time

import requests

BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:5000")

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_home_endpoint():
    """Test the home endpoint"""
    print("\nTesting home endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response preview: {response.text[:120]}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_single_prediction():
    """Test single transaction prediction"""
    print("\nTesting single transaction prediction...")
    
    # Sample transaction data (non-fraudulent)
    sample_transaction = {
        "V1": -1.3598071336738,
        "V2": -0.0727811733098497,
        "V3": 2.53634673796914,
        "V4": 1.37815522427443,
        "V5": -0.338320769942518,
        "V6": 0.462387777762292,
        "V7": 0.239598554061257,
        "V8": 0.0986979012610507,
        "V9": 0.363786969611213,
        "V10": 0.0907941719789316,
        "V11": -0.551599533260813,
        "V12": -0.617800855762348,
        "V13": -0.991389847235408,
        "V14": -0.311169353699879,
        "V15": 1.46817697209427,
        "V16": -0.470400525259478,
        "V17": 0.207971241929242,
        "V18": 0.0257905801985591,
        "V19": 0.403992960255733,
        "V20": 0.251412098239705,
        "V21": -0.018306777944153,
        "V22": 0.277837575558899,
        "V23": -0.110473910188767,
        "V24": 0.0669280749146731,
        "V25": 0.128539358273528,
        "V26": -0.189114843888824,
        "V27": 0.133558376740387,
        "V28": -0.0210530534538215,
        "Amount": 149.62
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            headers={"Content-Type": "application/json"},
            data=json.dumps(sample_transaction)
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_batch_prediction():
    """Test batch transaction prediction"""
    print("\nTesting batch transaction prediction...")
    
    # Sample batch data
    batch_data = {
        "transactions": [
            {
                "V1": -1.3598071336738,
                "V2": -0.0727811733098497,
                "V3": 2.53634673796914,
                "V4": 1.37815522427443,
                "V5": -0.338320769942518,
                "V6": 0.462387777762292,
                "V7": 0.239598554061257,
                "V8": 0.0986979012610507,
                "V9": 0.363786969611213,
                "V10": 0.0907941719789316,
                "V11": -0.551599533260813,
                "V12": -0.617800855762348,
                "V13": -0.991389847235408,
                "V14": -0.311169353699879,
                "V15": 1.46817697209427,
                "V16": -0.470400525259478,
                "V17": 0.207971241929242,
                "V18": 0.0257905801985591,
                "V19": 0.403992960255733,
                "V20": 0.251412098239705,
                "V21": -0.018306777944153,
                "V22": 0.277837575558899,
                "V23": -0.110473910188767,
                "V24": 0.0669280749146731,
                "V25": 0.128539358273528,
                "V26": -0.189114843888824,
                "V27": 0.133558376740387,
                "V28": -0.0210530534538215,
                "Amount": 149.62
            },
            {
                "V1": -0.0727811733098497,
                "V2": -1.3598071336738,
                "V3": 1.37815522427443,
                "V4": 2.53634673796914,
                "V5": 0.462387777762292,
                "V6": -0.338320769942518,
                "V7": 0.0986979012610507,
                "V8": 0.239598554061257,
                "V9": 0.0907941719789316,
                "V10": 0.363786969611213,
                "V11": -0.617800855762348,
                "V12": -0.551599533260813,
                "V13": -0.311169353699879,
                "V14": -0.991389847235408,
                "V15": -0.470400525259478,
                "V16": 1.46817697209427,
                "V17": 0.0257905801985591,
                "V18": 0.207971241929242,
                "V19": 0.251412098239705,
                "V20": 0.403992960255733,
                "V21": 0.277837575558899,
                "V22": -0.018306777944153,
                "V23": 0.0669280749146731,
                "V24": -0.110473910188767,
                "V25": -0.189114843888824,
                "V26": 0.128539358273528,
                "V27": -0.0210530534538215,
                "V28": 0.133558376740387,
                "Amount": 250.00
            }
        ]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict_batch",
            headers={"Content-Type": "application/json"},
            data=json.dumps(batch_data)
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_error_handling():
    """Test error handling with invalid data"""
    print("\nTesting error handling...")
    
    # Test with missing features
    invalid_data = {
        "V1": -1.3598071336738,
        "V2": -0.0727811733098497,
        # Missing other required features
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            headers={"Content-Type": "application/json"},
            data=json.dumps(invalid_data)
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 400  # Should return 400 for bad request
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing Fraud Detection API")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health_check),
        ("Home Endpoint", test_home_endpoint),
        ("Single Prediction", test_single_prediction),
        ("Batch Prediction", test_batch_prediction),
        ("Error Handling", test_error_handling)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        success = test_func()
        results.append((test_name, success))
        time.sleep(1)  # Small delay between tests
    
    print("\n" + "="*50)
    print("Test Results Summary")
    print("="*50)
    
    passed = 0
    for test_name, success in results:
        status = "PASS" if success else "FAIL"
        print(f"{test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("All tests passed! API is working correctly.")
    else:
        print("Some tests failed. Please check the API implementation.")

if __name__ == "__main__":
    main() 