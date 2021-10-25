#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid

## Security Orchestrator API Options ##
# Add Domain (POST /domains) --> # NOTE: NOT NECESSARY
# Retrieve Domains LIST (GET /domains) --> # NOTE: NOT NECESSARY
# Retrieve Domain (GET /domains/{domainId}) --> # NOTE: NOT NECESSARY
# Update Domain (PUT /domains/{domainId}) --> # NOTE: NOT NECESSARY
# Remove Domain (DELETE /domains/{domainId}) --> # NOTE: NOT NECESSARY


# Request New Policy Enforcement (POST /domains/{domainId}/policy-enforcements)

# Retrieve Policy Enforcements list (GET /domains/{domainId}/policy-enforcements)

# Retrieve Policy Enforcements State (GET /domains/{domainId}/policy-enforcements/{enforcementId})

# Undo Policy Enforcement (DELETE /domains/{domainId}/policy-enforcements/{enforcementId})

