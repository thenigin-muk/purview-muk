#!/bin/bash

# Ensure the directory exists
mkdir -p workflows/pcards

# Create the PCard metadata lists JSON
cat > workflows/pcards/metadata-lists.json <<EOL
{
  "lists": [
    {
      "name": "PCard Holders",
      "internal_name": "PCardHolders",
      "description": "Contains details about registered PCard users.",
      "columns": [
        {"name": "Cardholder Name", "internal_name": "CardholderName", "type": "Person or Group", "column_group": "PCard Columns"},
        {"name": "Supervisor Name", "internal_name": "SupervisorName", "type": "Person or Group", "column_group": "PCard Columns"},
        {"name": "Active?", "internal_name": "Active", "type": "Boolean", "column_group": "PCard Columns"}
      ]
    },
    {
      "name": "PCard Statement Dates",
      "internal_name": "PCardStatementDates",
      "description": "Tracks the valid PCard statement submission dates.",
      "columns": [
        {"name": "Billing Cycle Close Date", "internal_name": "BillingCycleCloseDate", "type": "DateTime", "column_group": "PCard Columns"},
        {"name": "Statement Year", "internal_name": "StatementYear", "type": "Number", "column_group": "PCard Columns"},
        {"name": "Active?", "internal_name": "Active", "type": "Boolean", "column_group": "PCard Columns"}
      ]
    },
    {
      "name": "PCard Submissions",
      "internal_name": "PCardSubmissions",
      "description": "Tracks individual PCard statements submitted by users.",
      "columns": [
        {"name": "Cardholder Name", "internal_name": "CardholderName", "type": "Lookup", "lookup_list": "PCard Holders", "lookup_field": "Title", "column_group": "PCard Columns"},
        {"name": "Supervisor Name", "internal_name": "SupervisorName", "type": "Lookup", "lookup_list": "PCard Holders", "lookup_field": "Supervisor Name", "column_group": "PCard Columns"},
        {"name": "Billing Cycle Close Date", "internal_name": "BillingCycleCloseDate", "type": "DateTime", "column_group": "PCard Columns"},
        {"name": "Submission Status", "internal_name": "SubmissionStatus", "type": "Choice", "choices": ["Pending", "Submitted", "Approved", "Rejected"], "column_group": "PCard Columns"},
        {"name": "File Uploaded?", "internal_name": "FileUploaded", "type": "Boolean", "column_group": "PCard Columns"},
        {"name": "Signed Copy Received?", "internal_name": "SignedCopyReceived", "type": "Boolean", "column_group": "PCard Columns"},
        {"name": "Date Submitted", "internal_name": "DateSubmitted", "type": "DateTime", "column_group": "PCard Columns"}
      ]
    }
  ]
}
EOL

echo "✅ Metadata lists JSON for Pcards written to workflows/pcards/metadata-lists.json"
