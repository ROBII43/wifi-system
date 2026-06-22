#!/usr/bin/env python
"""
Integration tests for payment flow
Tests: transaction creation -> STK push -> webhook -> activation
"""
import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Setup path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

from billing.service import create_guest_transaction, handle_webhook_payload
from billing.transactions import get_transaction, get_all_transactions


class TestPaymentFlow:
    """Test the complete payment flow"""

    @staticmethod
    def test_create_transaction():
        """Test 1: Create a guest transaction"""
        print("\n" + "="*60)
        print("TEST 1: Create Guest Transaction")
        print("="*60)

        result = create_guest_transaction(
            phone="254712345678",
            plan_id="plan_5mb",
            mac="AA:BB:CC:DD:EE:FF"
        )

        assert result["success"], f"Failed to create transaction: {result}"
        assert "txn_id" in result, "Missing txn_id in response"
        assert "phone" in result, "Missing phone in response"
        assert "amount" in result, "Missing amount in response"

        txn_id = result["txn_id"]
        print(f"✅ Transaction created: {txn_id}")
        print(f"   Phone: {result['phone']}")
        print(f"   Plan: {result['plan']}")
        print(f"   Amount: {result['amount']}")

        # Verify in database
        txn = get_transaction(txn_id)
        assert txn is not None, f"Transaction {txn_id} not found in database"
        assert txn["status"] == "pending", f"Transaction status should be 'pending', got {txn['status']}"
        print(f"✅ Transaction verified in database")

        return txn_id

    @staticmethod
    def test_webhook_success(txn_id):
        """Test 2: Handle successful webhook callback"""
        print("\n" + "="*60)
        print("TEST 2: Handle Webhook Success")
        print("="*60)

        # Simulate Lipana webhook payload
        webhook_payload = {
            "transactionId": txn_id,
            "status": "success",
            "phone": "254712345678",
            "amount": 100,
            "receipt": "TEST_RECEIPT_123",
            "transactionCode": "LIPANA_CODE_456"
        }

        print(f"Webhook payload: {webhook_payload}")

        result = handle_webhook_payload(webhook_payload)

        assert result["success"], f"Webhook handling failed: {result}"
        assert "transaction_id" in result, "Missing transaction_id in response"
        print(f"✅ Webhook processed successfully")
        print(f"   Transaction ID: {result['transaction_id']}")

        # Verify transaction was updated
        txn = get_transaction(txn_id)
        assert txn is not None, f"Transaction {txn_id} not found after webhook"
        assert txn["status"] == "success", f"Transaction status should be 'success', got {txn['status']}"
        assert txn["active"] == 1, f"Transaction should be active"
        assert txn["paid_at"] is not None, "paid_at should be set"
        assert txn["mikrotik_username"] is not None, "MikroTik username should be set"
        print(f"✅ Transaction activated")
        print(f"   Status: {txn['status']}")
        print(f"   Active: {txn['active']}")
        print(f"   MikroTik User: {txn['mikrotik_username']}")
        print(f"   Expiry: {txn['expiry']}")

    @staticmethod
    def test_webhook_failure(txn_id):
        """Test 3: Handle failed webhook callback"""
        print("\n" + "="*60)
        print("TEST 3: Handle Webhook Failure")
        print("="*60)

        # Create a new transaction for failure test
        result = create_guest_transaction(
            phone="254787654321",
            plan_id="plan_10mb",
            mac="AA:BB:CC:DD:EE:11"
        )
        txn_id = result["txn_id"]

        # Simulate failed Lipana webhook payload
        webhook_payload = {
            "transactionId": txn_id,
            "status": "failed",
            "phone": "254787654321",
            "amount": 200
        }

        print(f"Webhook payload: {webhook_payload}")

        result = handle_webhook_payload(webhook_payload)

        assert result["success"], f"Webhook handling failed: {result}"
        print(f"✅ Webhook processed successfully")

        # Verify transaction was marked as failed
        txn = get_transaction(txn_id)
        assert txn is not None, f"Transaction {txn_id} not found after webhook"
        assert txn["status"] == "failed", f"Transaction status should be 'failed', got {txn['status']}"
        print(f"✅ Transaction marked as failed")
        print(f"   Status: {txn['status']}")

    @staticmethod
    def test_webhook_missing_txn():
        """Test 4: Handle webhook for non-existent transaction"""
        print("\n" + "="*60)
        print("TEST 4: Handle Webhook for Missing Transaction")
        print("="*60)

        # Try to process webhook for non-existent transaction
        webhook_payload = {
            "transactionId": "TXN_NONEXISTENT_123456",
            "status": "success",
            "phone": "254712345678",
            "amount": 100
        }

        print(f"Webhook payload: {webhook_payload}")

        result = handle_webhook_payload(webhook_payload)

        assert not result["success"], f"Should fail for missing transaction"
        assert "not found" in result["message"].lower(), f"Message should mention 'not found', got: {result['message']}"
        print(f"✅ Correctly rejected webhook for missing transaction")
        print(f"   Message: {result['message']}")

    @staticmethod
    def run_all_tests():
        """Run all integration tests"""
        print("\n" + "="*80)
        print(" WIFI SYSTEM - PAYMENT FLOW INTEGRATION TESTS")
        print("="*80)

        try:
            # Test 1: Create transaction
            txn_id = TestPaymentFlow.test_create_transaction()

            # Test 2: Webhook success
            TestPaymentFlow.test_webhook_success(txn_id)

            # Test 3: Webhook failure
            TestPaymentFlow.test_webhook_failure(txn_id)

            # Test 4: Webhook missing transaction
            TestPaymentFlow.test_webhook_missing_txn()

            print("\n" + "="*80)
            print(" ✅ ALL TESTS PASSED")
            print("="*80)
            return True

        except AssertionError as e:
            print(f"\n❌ TEST FAILED: {e}")
            return False

        except Exception as e:
            print(f"\n❌ TEST ERROR: {e}")
            import traceback
            traceback.print_exc()
            return False


if __name__ == "__main__":
    success = TestPaymentFlow.run_all_tests()
    sys.exit(0 if success else 1)
