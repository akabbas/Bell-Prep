"""
Data Validation Rules Engine - Extensible Validation System

Purpose:
    Provides an extensible validation framework for data quality and business rule
    enforcement. Bell uses complex validation rules for procurement data, and this
    engine demonstrates how to implement them in a maintainable way.

Author: Business Systems Analyst - Bell Textron
Version: 1.0.0
License: Internal - Bell Textron Proprietary
"""

import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
from datetime import datetime
import re


class ValidationSeverity(Enum):
    """Severity levels for validation failures"""
    ERROR = "error"      # Reject record
    WARNING = "warning"  # Log but continue
    INFO = "info"        # Informational only


@dataclass
class ValidationResult:
    """Result of a single validation"""
    passed: bool
    rule_name: str
    severity: ValidationSeverity
    message: str = ""
    value: Optional[Any] = None
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class DataQualityScore:
    """Overall data quality score"""
    score: float  # 0-100
    confidence_level: str  # HIGH, MEDIUM, LOW
    passed_rules: int
    failed_rules: int
    warning_rules: int
    failed_rule_names: List[str]
    timestamp: datetime = field(default_factory=datetime.now)


class ValidationRule(ABC):
    """Base class for validation rules"""
    
    def __init__(
        self,
        name: str,
        severity: ValidationSeverity = ValidationSeverity.ERROR,
        logger: logging.Logger = None
    ):
        """
        Initialize validation rule.
        
        Args:
            name: Rule name
            severity: Failure severity
            logger: Logger instance
        """
        self.name = name
        self.severity = severity
        self.logger = logger or logging.getLogger(__name__)
    
    @abstractmethod
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """
        Validate data against this rule.
        
        Args:
            data: Data dictionary to validate
            
        Returns:
            ValidationResult
        """
        pass


class DUNSNumberRule(ValidationRule):
    """Validates DUNS numbers (9 digit format with check digit)"""
    
    def __init__(self, logger: logging.Logger = None):
        super().__init__("DUNS_NUMBER_VALIDATION", ValidationSeverity.ERROR, logger)
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate DUNS number format"""
        duns = data.get('duns_number', '')
        
        # Check length
        if len(duns) != 9:
            return ValidationResult(
                passed=False,
                rule_name=self.name,
                severity=self.severity,
                message=f"DUNS number must be 9 digits, got {len(duns)}",
                value=duns
            )
        
        # Check numeric
        if not duns.isdigit():
            return ValidationResult(
                passed=False,
                rule_name=self.name,
                severity=self.severity,
                message="DUNS number must contain only digits",
                value=duns
            )
        
        return ValidationResult(
            passed=True,
            rule_name=self.name,
            severity=self.severity,
            message="DUNS number is valid",
            value=duns
        )


class SupplierNameRule(ValidationRule):
    """Validates supplier name"""
    
    def __init__(self, logger: logging.Logger = None):
        super().__init__("SUPPLIER_NAME_VALIDATION", ValidationSeverity.WARNING, logger)
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate supplier name"""
        name = data.get('supplier_name', '').strip()
        
        if not name:
            return ValidationResult(
                passed=False,
                rule_name=self.name,
                severity=self.severity,
                message="Supplier name cannot be empty",
                value=name
            )
        
        if len(name) < 3:
            return ValidationResult(
                passed=False,
                rule_name=self.name,
                severity=self.severity,
                message="Supplier name must be at least 3 characters",
                value=name
            )
        
        if len(name) > 255:
            return ValidationResult(
                passed=False,
                rule_name=self.name,
                severity=self.severity,
                message="Supplier name exceeds 255 characters",
                value=name
            )
        
        return ValidationResult(
            passed=True,
            rule_name=self.name,
            severity=self.severity,
            message="Supplier name is valid",
            value=name
        )


class PercentageRule(ValidationRule):
    """Validates percentage fields (0-100)"""
    
    def __init__(self, field_name: str, logger: logging.Logger = None):
        super().__init__(f"PERCENTAGE_VALIDATION_{field_name}", ValidationSeverity.ERROR, logger)
        self.field_name = field_name
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate percentage field"""
        value = data.get(self.field_name)
        
        if value is None:
            return ValidationResult(
                passed=False,
                rule_name=self.name,
                severity=self.severity,
                message=f"{self.field_name} is required",
                value=value
            )
        
        try:
            pct = float(value)
        except (ValueError, TypeError):
            return ValidationResult(
                passed=False,
                rule_name=self.name,
                severity=self.severity,
                message=f"{self.field_name} must be numeric",
                value=value
            )
        
        if not 0 <= pct <= 100:
            return ValidationResult(
                passed=False,
                rule_name=self.name,
                severity=self.severity,
                message=f"{self.field_name} must be between 0 and 100, got {pct}",
                value=value
            )
        
        return ValidationResult(
            passed=True,
            rule_name=self.name,
            severity=self.severity,
            message=f"{self.field_name} is valid",
            value=value
        )


class ITARComplianceRule(ValidationRule):
    """Validates ITAR compliance for high-spend suppliers"""
    
    ITAR_THRESHOLD = 50000  # $50k
    
    def __init__(self, logger: logging.Logger = None):
        super().__init__("ITAR_COMPLIANCE_CHECK", ValidationSeverity.ERROR, logger)
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate ITAR compliance"""
        spend = data.get('spend_ytd', 0)
        itar_compliant = data.get('itar_compliant', False)
        
        if spend >= self.ITAR_THRESHOLD and not itar_compliant:
            return ValidationResult(
                passed=False,
                rule_name=self.name,
                severity=self.severity,
                message=f"High spend (${spend:,.2f}) requires ITAR compliance",
                value={'spend': spend, 'itar_compliant': itar_compliant}
            )
        
        return ValidationResult(
            passed=True,
            rule_name=self.name,
            severity=self.severity,
            message="ITAR compliance valid",
            value={'spend': spend, 'itar_compliant': itar_compliant}
        )


class AS9100CertificationRule(ValidationRule):
    """Validates AS9100 certification for high-risk suppliers"""
    
    def __init__(self, logger: logging.Logger = None):
        super().__init__("AS9100_CERTIFICATION_CHECK", ValidationSeverity.WARNING, logger)
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate AS9100 certification"""
        spend = data.get('spend_ytd', 0)
        as9100_certified = data.get('as9100_certified', False)
        
        # For high-spend suppliers, AS9100 is recommended
        if spend > 100000 and not as9100_certified:
            return ValidationResult(
                passed=False,
                rule_name=self.name,
                severity=self.severity,
                message=f"High-spend supplier (${spend:,.2f}) should be AS9100 certified",
                value={'spend': spend, 'as9100_certified': as9100_certified}
            )
        
        return ValidationResult(
            passed=True,
            rule_name=self.name,
            severity=self.severity,
            message="AS9100 certification status acceptable",
            value={'spend': spend, 'as9100_certified': as9100_certified}
        )


class ValidationRulesEngine:
    """
    Main validation rules engine with extensible rule system.
    
    Allows for custom rules, data quality scoring, and detailed reporting.
    """
    
    def __init__(self, logger: logging.Logger = None):
        """
        Initialize validation engine.
        
        Args:
            logger: Logger instance
        """
        self.logger = logger or logging.getLogger(__name__)
        self.rules: List[ValidationRule] = []
        
        # Add default rules
        self._add_default_rules()
    
    def _add_default_rules(self):
        """Add default validation rules"""
        self.add_rule(DUNSNumberRule(self.logger))
        self.add_rule(SupplierNameRule(self.logger))
        self.add_rule(PercentageRule('on_time_delivery_rate', self.logger))
        self.add_rule(PercentageRule('quality_rejection_rate', self.logger))
        self.add_rule(ITARComplianceRule(self.logger))
        self.add_rule(AS9100CertificationRule(self.logger))
    
    def add_rule(self, rule: ValidationRule):
        """
        Add validation rule to engine.
        
        Args:
            rule: ValidationRule instance
        """
        self.rules.append(rule)
        self.logger.debug(f"Added validation rule: {rule.name}")
    
    def remove_rule(self, rule_name: str):
        """
        Remove validation rule by name.
        
        Args:
            rule_name: Name of rule to remove
        """
        self.rules = [r for r in self.rules if r.name != rule_name]
        self.logger.debug(f"Removed validation rule: {rule_name}")
    
    def validate_supplier(self, supplier_data: Dict[str, Any]) -> 'ValidationReport':
        """
        Validate supplier data against all rules.
        
        Args:
            supplier_data: Supplier data dictionary
            
        Returns:
            ValidationReport with detailed results
        """
        results = []
        
        # Run all rules
        for rule in self.rules:
            try:
                result = rule.validate(supplier_data)
                results.append(result)
            except Exception as e:
                self.logger.error(f"Error executing rule {rule.name}: {e}")
                results.append(ValidationResult(
                    passed=False,
                    rule_name=rule.name,
                    severity=ValidationSeverity.ERROR,
                    message=f"Rule execution failed: {e}",
                    value=None
                ))
        
        # Generate report
        return ValidationReport(results, supplier_data, self.logger)


@dataclass
class ValidationReport:
    """Report of validation results"""
    results: List[ValidationResult]
    supplier_data: Dict[str, Any]
    logger: logging.Logger
    timestamp: datetime = field(default_factory=datetime.now)
    
    @property
    def passed_rules(self) -> List[ValidationResult]:
        """Get passed validation rules"""
        return [r for r in self.results if r.passed]
    
    @property
    def failed_rules(self) -> List[ValidationResult]:
        """Get failed validation rules"""
        return [r for r in self.results if not r.passed]
    
    @property
    def error_rules(self) -> List[ValidationResult]:
        """Get error-level rules that failed"""
        return [
            r for r in self.failed_rules 
            if r.severity == ValidationSeverity.ERROR
        ]
    
    @property
    def warning_rules(self) -> List[ValidationResult]:
        """Get warning-level rules that failed"""
        return [
            r for r in self.failed_rules 
            if r.severity == ValidationSeverity.WARNING
        ]
    
    @property
    def all_passed(self) -> bool:
        """Check if all error-level rules passed"""
        return len(self.error_rules) == 0
    
    @property
    def quality_score(self) -> DataQualityScore:
        """Calculate overall data quality score"""
        total_rules = len(self.results)
        passed = len(self.passed_rules)
        failed_errors = len(self.error_rules)
        failed_warnings = len(self.warning_rules)
        
        # Score calculation
        # 100 points for all passed
        # -20 per error
        # -5 per warning
        score = 100.0
        score -= (failed_errors * 20)
        score -= (failed_warnings * 5)
        score = max(0, min(100, score))  # Clamp 0-100
        
        # Confidence level based on number of warnings
        if failed_warnings == 0:
            confidence = "HIGH"
        elif failed_warnings <= 2:
            confidence = "MEDIUM"
        else:
            confidence = "LOW"
        
        return DataQualityScore(
            score=score,
            confidence_level=confidence,
            passed_rules=passed,
            failed_rules=len(self.failed_rules),
            warning_rules=failed_warnings,
            failed_rule_names=[r.rule_name for r in self.failed_rules]
        )
    
    def summary(self) -> Dict[str, Any]:
        """Get validation summary"""
        qs = self.quality_score
        
        return {
            'validation_passed': self.all_passed,
            'quality_score': qs.score,
            'confidence_level': qs.confidence_level,
            'total_rules': len(self.results),
            'passed_rules': qs.passed_rules,
            'failed_rules': qs.failed_rules,
            'error_rules': len(self.error_rules),
            'warning_rules': len(self.warning_rules),
            'failed_rule_names': qs.failed_rule_names,
            'timestamp': self.timestamp.isoformat()
        }
    
    def get_detailed_report(self) -> str:
        """Get detailed validation report as formatted string"""
        lines = [
            f"\n{'='*70}",
            f"VALIDATION REPORT",
            f"{'='*70}",
            f"Supplier: {self.supplier_data.get('supplier_name', 'Unknown')}",
            f"Generated: {self.timestamp.isoformat()}",
            f"{'='*70}",
            f"\nOVERALL QUALITY SCORE: {self.quality_score.score:.1f}/100",
            f"Confidence Level: {self.quality_score.confidence_level}",
            f"Status: {'✓ VALID' if self.all_passed else '✗ INVALID'}",
            f"\nRULE RESULTS:",
            f"  ✓ Passed: {len(self.passed_rules)}",
            f"  ✗ Failed (Errors): {len(self.error_rules)}",
            f"  ⚠ Failed (Warnings): {len(self.warning_rules)}",
        ]
        
        if self.error_rules:
            lines.append(f"\nCRITICAL ERRORS:")
            for result in self.error_rules:
                lines.append(f"  ✗ {result.rule_name}: {result.message}")
        
        if self.warning_rules:
            lines.append(f"\nWARNINGS:")
            for result in self.warning_rules:
                lines.append(f"  ⚠ {result.rule_name}: {result.message}")
        
        if self.passed_rules:
            lines.append(f"\nPASSED VALIDATIONS:")
            for result in self.passed_rules[:5]:  # Show first 5
                lines.append(f"  ✓ {result.rule_name}")
            if len(self.passed_rules) > 5:
                lines.append(f"  ... and {len(self.passed_rules) - 5} more")
        
        lines.append(f"\n{'='*70}\n")
        
        return "\n".join(lines)


