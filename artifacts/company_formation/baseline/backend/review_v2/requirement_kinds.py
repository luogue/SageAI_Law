"""Separate contractual evidence from legal defaults and external diligence.

Kinds are declared per element, never inferred from a citation being present.
External facts are not established by a promise to perform a check.
"""
from copy import deepcopy

CONTRACT_TERM = 'CONTRACT_TERM'
STATUTORY_DEFAULT = 'STATUTORY_DEFAULT'
EXTERNAL_VERIFICATION = 'EXTERNAL_VERIFICATION'
EXTERNAL_FACT_TYPES = {'external_fact','authorization_validity','corporate_resolution_validity','actual_delivery','actual_registration','actual_payment','actual_review','actual_approval','actual_possession'}

def partition(requirements):
    contractual, assessments = [], []
    for original in requirements:
        row = deepcopy(original)
        kind = EXTERNAL_VERIFICATION if row.get('fact_type') in EXTERNAL_FACT_TYPES else row.get('requirement_kind', CONTRACT_TERM)
        if kind == CONTRACT_TERM:
            contractual.append(row)
            continue
        if kind not in {STATUTORY_DEFAULT, EXTERNAL_VERIFICATION}:
            raise ValueError('Unknown requirement kind: ' + kind)
        if kind == STATUTORY_DEFAULT and not row.get('statutory_protection'):
            raise ValueError('A statutory default requires a direct legal proposition')
        assessments.append({
            'element_id': row['element_id'], 'target_element': row['proposition'],
            'requirement_kind': kind, 'contract_coverage_required': False,
            'status': 'PROTECTED_BY_LAW' if kind == STATUTORY_DEFAULT else 'PENDING_VERIFICATION',
            'legal_basis': row.get('legal_basis', ''),
            'statutory_protection': row.get('statutory_protection', ''),
            'verification_instruction': row.get('verification_instruction', ''),
            'verification_priority': row.get('verification_priority', 'LOW'),
            'risk_relevant': False,
            'fact_type': row.get('fact_type', ''),
            'external_fact_status': 'UNVERIFIED' if kind == EXTERNAL_VERIFICATION else None,
        })
    return contractual, assessments

def notes(assessments):
    return '；'.join(row['statutory_protection'] if row['requirement_kind']==STATUTORY_DEFAULT
        else row['verification_instruction'] for row in assessments)
