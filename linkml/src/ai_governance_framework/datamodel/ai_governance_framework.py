# Auto generated from ai_governance_framework.yaml by pythongen.py version: 0.0.1
# Generation date: 2026-06-25T01:10:05
# Schema: ai-governance-framework
#
# id: https://w3id.org/lmodel/ai-governance-framework
# description: A FINOS-curated instance dataset of the ai-atlas-nexus [`ai-risk-ontology`](https://github.com/finos/ai-governance-framework).
#
#   The [schema](https://github.com/lmodel/ai-governance-framework/blob/main/linkml/src/ai_governance_framework/schema/ai_governance_framework.yaml) and
#   cross-walked to ISO 42001 / NIST AI 600-1 / DPV / AIRO / OWASP via
#   SSSOM mapping files under `/src/ai_governance_framework/mappings/`.
#
#   The [ai-atlas-nexus](https://ibm.github.io/ai-atlas-nexus/) upstream is vendored under `./ai_risk_ontology/`
#   until the `https://w3id.org/ai-atlas-nexus/` redirect goes live.'
# license: Apache-2.0

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import Boolean, Date, Datetime, Float, Integer, String, Uri
from linkml_runtime.utils.metamodelcore import Bool, URI, XSDDate, XSDDateTime

metamodel_version = "1.11.0"
version = "0.1.0"

# Namespaces
AI = CurieNamespace('ai', 'https://w3id.org/dpv/ai#')
AI_GOVERNANCE_FRAMEWORK = CurieNamespace('ai_governance_framework', 'https://w3id.org/lmodel/ai-governance-framework/')
AIRO = CurieNamespace('airo', 'https://w3id.org/airo#')
DCT = CurieNamespace('dct', 'http://purl.org/dc/terms/')
DPV = CurieNamespace('dpv', 'https://w3id.org/dpv#')
DPV_RISK = CurieNamespace('dpv_risk', 'https://w3id.org/dpv/risk#')
DQV = CurieNamespace('dqv', 'https://www.w3.org/TR/vocab-dqv/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
NEXUS = CurieNamespace('nexus', 'https://w3id.org/ai-atlas-nexus/')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
TECH = CurieNamespace('tech', 'https://w3id.org/dpv/tech#')
DEFAULT_ = AI_GOVERNANCE_FRAMEWORK


# Types

# Class references
class EntityId(extended_str):
    pass


class OrganizationId(EntityId):
    pass


class LicenseId(EntityId):
    pass


class DatasetId(EntityId):
    pass


class DocumentationId(EntityId):
    pass


class VocabularyId(EntityId):
    pass


class TaxonomyId(EntityId):
    pass


class ConceptId(EntityId):
    pass


class ControlId(EntityId):
    pass


class GroupId(EntityId):
    pass


class EntryId(EntityId):
    pass


class TermId(EntryId):
    pass


class PrincipleId(EntryId):
    pass


class PolicyId(EntityId):
    pass


class LLMQuestionPolicyId(PolicyId):
    pass


class RuleId(EntityId):
    pass


class AttributeConditionRuleId(RuleId):
    pass


class PermissionId(RuleId):
    pass


class ProhibitionId(RuleId):
    pass


class ObligationId(RuleId):
    pass


class RecommendationId(RuleId):
    pass


class CertificationId(EntryId):
    pass


class RiskTaxonomyId(TaxonomyId):
    pass


class RiskControlGroupTaxonomyId(TaxonomyId):
    pass


class RiskControlGroupId(GroupId):
    pass


class RiskGroupId(GroupId):
    pass


class RiskId(EntryId):
    pass


class RiskConceptId(ConceptId):
    pass


class RiskControlId(ControlId):
    pass


class ActionId(RiskControlId):
    pass


class RiskIncidentId(EntityId):
    pass


class ImpactId(EntityId):
    pass


class IncidentStatusId(EntityId):
    pass


class IncidentConcludedclassId(IncidentStatusId):
    pass


class IncidentHaltedclassId(IncidentStatusId):
    pass


class IncidentMitigatedclassId(IncidentStatusId):
    pass


class IncidentNearMissclassId(IncidentStatusId):
    pass


class IncidentOngoingclassId(IncidentStatusId):
    pass


class SeverityId(EntityId):
    pass


class LikelihoodId(EntityId):
    pass


class ConsequenceId(EntityId):
    pass


class CapabilityTaxonomyId(TaxonomyId):
    pass


class CapabilityConceptId(ConceptId):
    pass


class CapabilityDomainId(GroupId):
    pass


class CapabilityGroupId(GroupId):
    pass


class CapabilityId(EntryId):
    pass


class BaseAiId(EntityId):
    pass


class AiSystemId(EntryId):
    pass


class AiAgentId(AiSystemId):
    pass


class AiModelId(BaseAiId):
    pass


class LargeLanguageModelId(AiModelId):
    pass


class LargeLanguageModelFamilyId(EntityId):
    pass


class AiTaskId(EntryId):
    pass


class AiTaskTaxonomyId(TaxonomyId):
    pass


class AiTaskDomainId(GroupId):
    pass


class AiTaskGroupId(GroupId):
    pass


class AiLifecyclePhaseId(EntityId):
    pass


class DataPreprocessingId(AiLifecyclePhaseId):
    pass


class AiModelValidationId(AiLifecyclePhaseId):
    pass


class AiProviderId(OrganizationId):
    pass


class ModalityId(EntityId):
    pass


class InputId(EntityId):
    pass


class PurposeId(EntryId):
    pass


class DomainId(EntryId):
    pass


class LocalityOfUseId(EntryId):
    pass


class AIComponentId(EntityId):
    pass


class StakeholderId(EntityId):
    pass


class AISubjectId(StakeholderId):
    pass


class AIOperatorId(StakeholderId):
    pass


class AIDeveloperId(StakeholderId):
    pass


class AIDeployerId(AIOperatorId):
    pass


class AIUserId(StakeholderId):
    pass


class StakeholderGroupId(GroupId):
    pass


class AiEvalId(EntityId):
    pass


class AiEvalResultId(EntityId):
    pass


class SourceMetadataId(EntityId):
    pass


class ModelInfoId(EntityId):
    pass


class SourceDataId(EntityId):
    pass


class MetricConfigId(EntityId):
    pass


class ScoreDetailsId(EntityId):
    pass


class EvaluationResultRecordId(EntityId):
    pass


class EveryEvalAIResultId(AiEvalResultId):
    pass


class BenchmarkMetadataCardId(EntityId):
    pass


class QuestionId(AiEvalId):
    pass


class QuestionnaireId(AiEvalId):
    pass


class AdapterId(EntryId):
    pass


class LLMIntrinsicId(EntryId):
    pass


class ControlActivityId(RuleId):
    pass


class ControlActivityPermissionId(PermissionId):
    pass


class ControlActivityProhibitionId(ProhibitionId):
    pass


class ControlActivityObligationId(ObligationId):
    pass


class ControlActivityRecommendationId(RecommendationId):
    pass


class RequirementId(RuleId):
    pass


class AiOfficeId(OrganizationId):
    pass


@dataclass(repr=False)
class Container(YAMLRoot):
    """
    An umbrella object that holds the ontology class instances
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["Container"]
    class_class_curie: ClassVar[str] = "nexus:Container"
    class_name: ClassVar[str] = "Container"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.Container

    organizations: Optional[Union[dict[Union[str, OrganizationId], Union[dict, "Organization"]], list[Union[dict, "Organization"]]]] = empty_dict()
    licenses: Optional[Union[dict[Union[str, LicenseId], Union[dict, "License"]], list[Union[dict, "License"]]]] = empty_dict()
    modalities: Optional[Union[dict[Union[str, ModalityId], Union[dict, "Modality"]], list[Union[dict, "Modality"]]]] = empty_dict()
    aitasks: Optional[Union[dict[Union[str, AiTaskId], Union[dict, "AiTask"]], list[Union[dict, "AiTask"]]]] = empty_dict()
    documents: Optional[Union[dict[Union[str, DocumentationId], Union[dict, "Documentation"]], list[Union[dict, "Documentation"]]]] = empty_dict()
    datasets: Optional[Union[dict[Union[str, DatasetId], Union[dict, "Dataset"]], list[Union[dict, "Dataset"]]]] = empty_dict()
    llmintrinsics: Optional[Union[dict[Union[str, LLMIntrinsicId], Union[dict, "LLMIntrinsic"]], list[Union[dict, "LLMIntrinsic"]]]] = empty_dict()
    adapters: Optional[Union[dict[Union[str, AdapterId], Union[dict, "Adapter"]], list[Union[dict, "Adapter"]]]] = empty_dict()
    taxonomies: Optional[Union[dict[Union[str, TaxonomyId], Union[dict, "Taxonomy"]], list[Union[dict, "Taxonomy"]]]] = empty_dict()
    concepts: Optional[Union[dict[Union[str, ConceptId], Union[dict, "Concept"]], list[Union[dict, "Concept"]]]] = empty_dict()
    entries: Optional[Union[dict[Union[str, EntryId], Union[dict, "Entry"]], list[Union[dict, "Entry"]]]] = empty_dict()
    groups: Optional[Union[dict[Union[str, GroupId], Union[dict, "Group"]], list[Union[dict, "Group"]]]] = empty_dict()
    vocabularies: Optional[Union[dict[Union[str, VocabularyId], Union[dict, "Vocabulary"]], list[Union[dict, "Vocabulary"]]]] = empty_dict()
    controls: Optional[Union[dict[Union[str, ControlId], Union[dict, "Control"]], list[Union[dict, "Control"]]]] = empty_dict()
    riskincidents: Optional[Union[dict[Union[str, RiskIncidentId], Union[dict, "RiskIncident"]], list[Union[dict, "RiskIncident"]]]] = empty_dict()
    stakeholdergroups: Optional[Union[dict[Union[str, StakeholderGroupId], Union[dict, "StakeholderGroup"]], list[Union[dict, "StakeholderGroup"]]]] = empty_dict()
    stakeholders: Optional[Union[dict[Union[str, StakeholderId], Union[dict, "Stakeholder"]], list[Union[dict, "Stakeholder"]]]] = empty_dict()
    actions: Optional[Union[dict[Union[str, ActionId], Union[dict, "Action"]], list[Union[dict, "Action"]]]] = empty_dict()
    evaluations: Optional[Union[dict[Union[str, AiEvalId], Union[dict, "AiEval"]], list[Union[dict, "AiEval"]]]] = empty_dict()
    aievalresults: Optional[Union[dict[Union[str, AiEvalResultId], Union[dict, "AiEvalResult"]], list[Union[dict, "AiEvalResult"]]]] = empty_dict()
    benchmarkmetadatacards: Optional[Union[dict[Union[str, BenchmarkMetadataCardId], Union[dict, "BenchmarkMetadataCard"]], list[Union[dict, "BenchmarkMetadataCard"]]]] = empty_dict()
    aimodelfamilies: Optional[Union[dict[Union[str, LargeLanguageModelFamilyId], Union[dict, "LargeLanguageModelFamily"]], list[Union[dict, "LargeLanguageModelFamily"]]]] = empty_dict()
    aimodels: Optional[Union[dict[Union[str, LargeLanguageModelId], Union[dict, "LargeLanguageModel"]], list[Union[dict, "LargeLanguageModel"]]]] = empty_dict()
    policies: Optional[Union[dict[Union[str, PolicyId], Union[dict, "Policy"]], list[Union[dict, "Policy"]]]] = empty_dict()
    rules: Optional[Union[dict[Union[str, RuleId], Union[dict, "Rule"]], list[Union[dict, "Rule"]]]] = empty_dict()
    prohibitions: Optional[Union[dict[Union[str, ProhibitionId], Union[dict, "Prohibition"]], list[Union[dict, "Prohibition"]]]] = empty_dict()
    permissions: Optional[Union[dict[Union[str, PermissionId], Union[dict, "Permission"]], list[Union[dict, "Permission"]]]] = empty_dict()
    obligations: Optional[Union[dict[Union[str, ObligationId], Union[dict, "Obligation"]], list[Union[dict, "Obligation"]]]] = empty_dict()

    def __post_init__(self, *_: str, **kwargs: Any):
        self._normalize_inlined_as_list(slot_name="organizations", slot_type=Organization, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="licenses", slot_type=License, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="modalities", slot_type=Modality, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="aitasks", slot_type=AiTask, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="documents", slot_type=Documentation, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="datasets", slot_type=Dataset, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="llmintrinsics", slot_type=LLMIntrinsic, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="adapters", slot_type=Adapter, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="taxonomies", slot_type=Taxonomy, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="concepts", slot_type=Concept, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="entries", slot_type=Entry, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="groups", slot_type=Group, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="vocabularies", slot_type=Vocabulary, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="controls", slot_type=Control, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="riskincidents", slot_type=RiskIncident, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="stakeholdergroups", slot_type=StakeholderGroup, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="stakeholders", slot_type=Stakeholder, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="actions", slot_type=Action, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="evaluations", slot_type=AiEval, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="aievalresults", slot_type=AiEvalResult, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="benchmarkmetadatacards", slot_type=BenchmarkMetadataCard, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="aimodelfamilies", slot_type=LargeLanguageModelFamily, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="aimodels", slot_type=LargeLanguageModel, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="policies", slot_type=Policy, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="rules", slot_type=Rule, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="prohibitions", slot_type=Prohibition, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="permissions", slot_type=Permission, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="obligations", slot_type=Obligation, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Entity(YAMLRoot):
    """
    A generic grouping for any identifiable entity.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCHEMA["Thing"]
    class_class_curie: ClassVar[str] = "schema:Thing"
    class_name: ClassVar[str] = "Entity"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.Entity

    id: Union[str, EntityId] = None
    name: Optional[str] = None
    description: Optional[str] = None
    url: Optional[Union[str, URI]] = None
    dateCreated: Optional[Union[str, XSDDate]] = None
    dateModified: Optional[Union[str, XSDDate]] = None
    exact_mappings: Optional[Union[Union[dict, "Any"], list[Union[dict, "Any"]]]] = empty_list()
    close_mappings: Optional[Union[Union[dict, "Any"], list[Union[dict, "Any"]]]] = empty_list()
    related_mappings: Optional[Union[Union[dict, "Any"], list[Union[dict, "Any"]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[dict, "Any"], list[Union[dict, "Any"]]]] = empty_list()
    broad_mappings: Optional[Union[Union[dict, "Any"], list[Union[dict, "Any"]]]] = empty_list()
    isCategorizedAs: Optional[Union[Union[dict, "Any"], list[Union[dict, "Any"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, EntityId):
            self.id = EntityId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.url is not None and not isinstance(self.url, URI):
            self.url = URI(self.url)

        if self.dateCreated is not None and not isinstance(self.dateCreated, XSDDate):
            self.dateCreated = XSDDate(self.dateCreated)

        if self.dateModified is not None and not isinstance(self.dateModified, XSDDate):
            self.dateModified = XSDDate(self.dateModified)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Organization(Entity):
    """
    Any organizational entity such as a corporation, educational institution, consortium, government, etc.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCHEMA["Organization"]
    class_class_curie: ClassVar[str] = "schema:Organization"
    class_name: ClassVar[str] = "Organization"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.Organization

    id: Union[str, OrganizationId] = None
    grants_license: Optional[Union[str, LicenseId]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, OrganizationId):
            self.id = OrganizationId(self.id)

        if self.grants_license is not None and not isinstance(self.grants_license, LicenseId):
            self.grants_license = LicenseId(self.grants_license)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class License(Entity):
    """
    The general notion of a license which defines terms and grants permissions to users of AI systems, datasets and
    software.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AIRO["License"]
    class_class_curie: ClassVar[str] = "airo:License"
    class_name: ClassVar[str] = "License"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.License

    id: Union[str, LicenseId] = None
    version: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, LicenseId):
            self.id = LicenseId(self.id)

        if self.version is not None and not isinstance(self.version, str):
            self.version = str(self.version)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Dataset(Entity):
    """
    A body of structured information describing some topic(s) of interest.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCHEMA["Dataset"]
    class_class_curie: ClassVar[str] = "schema:Dataset"
    class_name: ClassVar[str] = "Dataset"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.Dataset

    id: Union[str, DatasetId] = None
    hasLicense: Optional[Union[str, LicenseId]] = None
    hasDocumentation: Optional[Union[Union[str, DocumentationId], list[Union[str, DocumentationId]]]] = empty_list()
    provider: Optional[Union[str, OrganizationId]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DatasetId):
            self.id = DatasetId(self.id)

        if self.hasLicense is not None and not isinstance(self.hasLicense, LicenseId):
            self.hasLicense = LicenseId(self.hasLicense)

        if not isinstance(self.hasDocumentation, list):
            self.hasDocumentation = [self.hasDocumentation] if self.hasDocumentation is not None else []
        self.hasDocumentation = [v if isinstance(v, DocumentationId) else DocumentationId(v) for v in self.hasDocumentation]

        if self.provider is not None and not isinstance(self.provider, OrganizationId):
            self.provider = OrganizationId(self.provider)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Documentation(Entity):
    """
    Documented information about a concept or other topic(s) of interest.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AIRO["Documentation"]
    class_class_curie: ClassVar[str] = "airo:Documentation"
    class_name: ClassVar[str] = "Documentation"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.Documentation

    id: Union[str, DocumentationId] = None
    hasLicense: Optional[Union[str, LicenseId]] = None
    hasJurisdiction: Optional[Union[Union[str, "Jurisdiction"], list[Union[str, "Jurisdiction"]]]] = empty_list()
    author: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DocumentationId):
            self.id = DocumentationId(self.id)

        if self.hasLicense is not None and not isinstance(self.hasLicense, LicenseId):
            self.hasLicense = LicenseId(self.hasLicense)

        if not isinstance(self.hasJurisdiction, list):
            self.hasJurisdiction = [self.hasJurisdiction] if self.hasJurisdiction is not None else []
        self.hasJurisdiction = [v if isinstance(v, Jurisdiction) else Jurisdiction(v) for v in self.hasJurisdiction]

        if self.author is not None and not isinstance(self.author, str):
            self.author = str(self.author)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Fact(YAMLRoot):
    """
    A fact about something, for example the result of a measurement. In addition to the value, evidence is provided.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCHEMA["Statement"]
    class_class_curie: ClassVar[str] = "schema:Statement"
    class_name: ClassVar[str] = "Fact"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.Fact

    value: str = None
    evidence: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.value):
            self.MissingRequiredField("value")
        if not isinstance(self.value, str):
            self.value = str(self.value)

        if self.evidence is not None and not isinstance(self.evidence, str):
            self.evidence = str(self.evidence)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Vocabulary(Entity):
    """
    A collection of terms, with their definitions and relationships.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SKOS["ConceptScheme"]
    class_class_curie: ClassVar[str] = "skos:ConceptScheme"
    class_name: ClassVar[str] = "Vocabulary"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.Vocabulary

    id: Union[str, VocabularyId] = None
    version: Optional[str] = None
    hasDocumentation: Optional[Union[Union[str, DocumentationId], list[Union[str, DocumentationId]]]] = empty_list()
    hasLicense: Optional[Union[str, LicenseId]] = None
    type: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.version is not None and not isinstance(self.version, str):
            self.version = str(self.version)

        if not isinstance(self.hasDocumentation, list):
            self.hasDocumentation = [self.hasDocumentation] if self.hasDocumentation is not None else []
        self.hasDocumentation = [v if isinstance(v, DocumentationId) else DocumentationId(v) for v in self.hasDocumentation]

        if self.hasLicense is not None and not isinstance(self.hasLicense, LicenseId):
            self.hasLicense = LicenseId(self.hasLicense)

        self.type = str(self.class_name)

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class Taxonomy(Entity):
    """
    A hierachical taxonomy of concepts, with their definitions and relationships.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SKOS["ConceptScheme"]
    class_class_curie: ClassVar[str] = "skos:ConceptScheme"
    class_name: ClassVar[str] = "Taxonomy"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.Taxonomy

    id: Union[str, TaxonomyId] = None
    version: Optional[str] = None
    hasDocumentation: Optional[Union[Union[str, DocumentationId], list[Union[str, DocumentationId]]]] = empty_list()
    hasLicense: Optional[Union[str, LicenseId]] = None
    type: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.version is not None and not isinstance(self.version, str):
            self.version = str(self.version)

        if not isinstance(self.hasDocumentation, list):
            self.hasDocumentation = [self.hasDocumentation] if self.hasDocumentation is not None else []
        self.hasDocumentation = [v if isinstance(v, DocumentationId) else DocumentationId(v) for v in self.hasDocumentation]

        if self.hasLicense is not None and not isinstance(self.hasLicense, LicenseId):
            self.hasLicense = LicenseId(self.hasLicense)

        self.type = str(self.class_name)

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


    def __new__(cls, *args, **kwargs):

        type_designator = "type"
        if not type_designator in kwargs:
            return super().__new__(cls,*args,**kwargs)
        else:
            type_designator_value = kwargs[type_designator]
            target_cls = cls._class_for("class_name", type_designator_value)


            if target_cls is None:
                raise ValueError(f"Wrong type designator value: class {cls.__name__} "
                                 f"has no subclass with ['class_name']='{kwargs[type_designator]}'")
            return super().__new__(target_cls,*args,**kwargs)



@dataclass(repr=False)
class Concept(Entity):
    """
    A concept
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SKOS["Concept"]
    class_class_curie: ClassVar[str] = "skos:Concept"
    class_name: ClassVar[str] = "Concept"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.Concept

    id: Union[str, ConceptId] = None
    isDefinedByTaxonomy: Optional[Union[str, TaxonomyId]] = None
    hasDocumentation: Optional[Union[Union[str, DocumentationId], list[Union[str, DocumentationId]]]] = empty_list()
    hasJurisdiction: Optional[Union[Union[str, "Jurisdiction"], list[Union[str, "Jurisdiction"]]]] = empty_list()
    type: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.isDefinedByTaxonomy is not None and not isinstance(self.isDefinedByTaxonomy, TaxonomyId):
            self.isDefinedByTaxonomy = TaxonomyId(self.isDefinedByTaxonomy)

        if not isinstance(self.hasDocumentation, list):
            self.hasDocumentation = [self.hasDocumentation] if self.hasDocumentation is not None else []
        self.hasDocumentation = [v if isinstance(v, DocumentationId) else DocumentationId(v) for v in self.hasDocumentation]

        if not isinstance(self.hasJurisdiction, list):
            self.hasJurisdiction = [self.hasJurisdiction] if self.hasJurisdiction is not None else []
        self.hasJurisdiction = [v if isinstance(v, Jurisdiction) else Jurisdiction(v) for v in self.hasJurisdiction]

        self.type = str(self.class_name)

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


    def __new__(cls, *args, **kwargs):

        type_designator = "type"
        if not type_designator in kwargs:
            return super().__new__(cls,*args,**kwargs)
        else:
            type_designator_value = kwargs[type_designator]
            target_cls = cls._class_for("class_name", type_designator_value)


            if target_cls is None:
                raise ValueError(f"Wrong type designator value: class {cls.__name__} "
                                 f"has no subclass with ['class_name']='{kwargs[type_designator]}'")
            return super().__new__(target_cls,*args,**kwargs)



@dataclass(repr=False)
class Control(Entity):
    """
    A measure that maintains and/or modifies
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["Control"]
    class_class_curie: ClassVar[str] = "nexus:Control"
    class_name: ClassVar[str] = "Control"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.Control

    id: Union[str, ControlId] = None
    isDefinedByTaxonomy: Optional[Union[str, TaxonomyId]] = None
    isApplicableinLocality: Optional[Union[Union[str, LocalityOfUseId], list[Union[str, LocalityOfUseId]]]] = empty_list()
    type: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.isDefinedByTaxonomy is not None and not isinstance(self.isDefinedByTaxonomy, TaxonomyId):
            self.isDefinedByTaxonomy = TaxonomyId(self.isDefinedByTaxonomy)

        if not isinstance(self.isApplicableinLocality, list):
            self.isApplicableinLocality = [self.isApplicableinLocality] if self.isApplicableinLocality is not None else []
        self.isApplicableinLocality = [v if isinstance(v, LocalityOfUseId) else LocalityOfUseId(v) for v in self.isApplicableinLocality]

        self.type = str(self.class_name)

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


    def __new__(cls, *args, **kwargs):

        type_designator = "type"
        if not type_designator in kwargs:
            return super().__new__(cls,*args,**kwargs)
        else:
            type_designator_value = kwargs[type_designator]
            target_cls = cls._class_for("class_name", type_designator_value)


            if target_cls is None:
                raise ValueError(f"Wrong type designator value: class {cls.__name__} "
                                 f"has no subclass with ['class_name']='{kwargs[type_designator]}'")
            return super().__new__(target_cls,*args,**kwargs)



@dataclass(repr=False)
class Group(Entity):
    """
    Labelled groups of concepts.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SKOS["Collection"]
    class_class_curie: ClassVar[str] = "skos:Collection"
    class_name: ClassVar[str] = "Group"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.Group

    id: Union[str, GroupId] = None
    isDefinedByTaxonomy: Optional[Union[str, TaxonomyId]] = None
    hasDocumentation: Optional[Union[Union[str, DocumentationId], list[Union[str, DocumentationId]]]] = empty_list()
    hasPart: Optional[Union[str, list[str]]] = empty_list()
    belongsToDomain: Optional[Union[dict, "Any"]] = None
    type: Optional[str] = "Group"
    narrower: Optional[Union[str, list[str]]] = empty_list()
    broader: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.isDefinedByTaxonomy is not None and not isinstance(self.isDefinedByTaxonomy, TaxonomyId):
            self.isDefinedByTaxonomy = TaxonomyId(self.isDefinedByTaxonomy)

        if not isinstance(self.hasDocumentation, list):
            self.hasDocumentation = [self.hasDocumentation] if self.hasDocumentation is not None else []
        self.hasDocumentation = [v if isinstance(v, DocumentationId) else DocumentationId(v) for v in self.hasDocumentation]

        if not isinstance(self.hasPart, list):
            self.hasPart = [self.hasPart] if self.hasPart is not None else []
        self.hasPart = [v if isinstance(v, str) else str(v) for v in self.hasPart]

        self.type = str(self.class_name)

        if not isinstance(self.narrower, list):
            self.narrower = [self.narrower] if self.narrower is not None else []
        self.narrower = [v if isinstance(v, str) else str(v) for v in self.narrower]

        if not isinstance(self.broader, list):
            self.broader = [self.broader] if self.broader is not None else []
        self.broader = [v if isinstance(v, str) else str(v) for v in self.broader]

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


    def __new__(cls, *args, **kwargs):

        type_designator = "type"
        if not type_designator in kwargs:
            return super().__new__(cls,*args,**kwargs)
        else:
            type_designator_value = kwargs[type_designator]
            target_cls = cls._class_for("class_name", type_designator_value)


            if target_cls is None:
                raise ValueError(f"Wrong type designator value: class {cls.__name__} "
                                 f"has no subclass with ['class_name']='{kwargs[type_designator]}'")
            return super().__new__(target_cls,*args,**kwargs)



@dataclass(repr=False)
class Entry(Entity):
    """
    An entry and its definitions.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["Entry"]
    class_class_curie: ClassVar[str] = "nexus:Entry"
    class_name: ClassVar[str] = "Entry"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.Entry

    id: Union[str, EntryId] = None
    isDefinedByTaxonomy: Optional[Union[str, TaxonomyId]] = None
    isDefinedByVocabulary: Optional[Union[str, VocabularyId]] = None
    hasDocumentation: Optional[Union[Union[str, DocumentationId], list[Union[str, DocumentationId]]]] = empty_list()
    isPartOf: Optional[str] = None
    requiredByTask: Optional[Union[Union[str, AiTaskId], list[Union[str, AiTaskId]]]] = empty_list()
    requiresCapability: Optional[Union[Union[str, CapabilityId], list[Union[str, CapabilityId]]]] = empty_list()
    implementedByAdapter: Optional[Union[Union[dict, "Any"], list[Union[dict, "Any"]]]] = empty_list()
    hasRule: Optional[Union[Union[str, RuleId], list[Union[str, RuleId]]]] = empty_list()
    type: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.isDefinedByTaxonomy is not None and not isinstance(self.isDefinedByTaxonomy, TaxonomyId):
            self.isDefinedByTaxonomy = TaxonomyId(self.isDefinedByTaxonomy)

        if self.isDefinedByVocabulary is not None and not isinstance(self.isDefinedByVocabulary, VocabularyId):
            self.isDefinedByVocabulary = VocabularyId(self.isDefinedByVocabulary)

        if not isinstance(self.hasDocumentation, list):
            self.hasDocumentation = [self.hasDocumentation] if self.hasDocumentation is not None else []
        self.hasDocumentation = [v if isinstance(v, DocumentationId) else DocumentationId(v) for v in self.hasDocumentation]

        if self.isPartOf is not None and not isinstance(self.isPartOf, str):
            self.isPartOf = str(self.isPartOf)

        if not isinstance(self.requiredByTask, list):
            self.requiredByTask = [self.requiredByTask] if self.requiredByTask is not None else []
        self.requiredByTask = [v if isinstance(v, AiTaskId) else AiTaskId(v) for v in self.requiredByTask]

        if not isinstance(self.requiresCapability, list):
            self.requiresCapability = [self.requiresCapability] if self.requiresCapability is not None else []
        self.requiresCapability = [v if isinstance(v, CapabilityId) else CapabilityId(v) for v in self.requiresCapability]

        if not isinstance(self.hasRule, list):
            self.hasRule = [self.hasRule] if self.hasRule is not None else []
        self.hasRule = [v if isinstance(v, RuleId) else RuleId(v) for v in self.hasRule]

        self.type = str(self.class_name)

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


    def __new__(cls, *args, **kwargs):

        type_designator = "type"
        if not type_designator in kwargs:
            return super().__new__(cls,*args,**kwargs)
        else:
            type_designator_value = kwargs[type_designator]
            target_cls = cls._class_for("class_name", type_designator_value)


            if target_cls is None:
                raise ValueError(f"Wrong type designator value: class {cls.__name__} "
                                 f"has no subclass with ['class_name']='{kwargs[type_designator]}'")
            return super().__new__(target_cls,*args,**kwargs)



@dataclass(repr=False)
class Term(Entry):
    """
    A term and its definitions.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["Term"]
    class_class_curie: ClassVar[str] = "nexus:Term"
    class_name: ClassVar[str] = "Term"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.Term

    id: Union[str, TermId] = None
    isDefinedByVocabulary: Optional[Union[str, VocabularyId]] = None
    hasDocumentation: Optional[Union[Union[str, DocumentationId], list[Union[str, DocumentationId]]]] = empty_list()
    hasParentDefinition: Optional[Union[Union[str, TermId], list[Union[str, TermId]]]] = empty_list()
    hasSubDefinition: Optional[Union[Union[str, TermId], list[Union[str, TermId]]]] = empty_list()
    hasRelatedRisk: Optional[Union[Union[str, RiskId], list[Union[str, RiskId]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, TermId):
            self.id = TermId(self.id)

        if self.isDefinedByVocabulary is not None and not isinstance(self.isDefinedByVocabulary, VocabularyId):
            self.isDefinedByVocabulary = VocabularyId(self.isDefinedByVocabulary)

        if not isinstance(self.hasDocumentation, list):
            self.hasDocumentation = [self.hasDocumentation] if self.hasDocumentation is not None else []
        self.hasDocumentation = [v if isinstance(v, DocumentationId) else DocumentationId(v) for v in self.hasDocumentation]

        if not isinstance(self.hasParentDefinition, list):
            self.hasParentDefinition = [self.hasParentDefinition] if self.hasParentDefinition is not None else []
        self.hasParentDefinition = [v if isinstance(v, TermId) else TermId(v) for v in self.hasParentDefinition]

        if not isinstance(self.hasSubDefinition, list):
            self.hasSubDefinition = [self.hasSubDefinition] if self.hasSubDefinition is not None else []
        self.hasSubDefinition = [v if isinstance(v, TermId) else TermId(v) for v in self.hasSubDefinition]

        if not isinstance(self.hasRelatedRisk, list):
            self.hasRelatedRisk = [self.hasRelatedRisk] if self.hasRelatedRisk is not None else []
        self.hasRelatedRisk = [v if isinstance(v, RiskId) else RiskId(v) for v in self.hasRelatedRisk]

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class Principle(Entry):
    """
    A representation of values or norms that must be taken into consideration when conducting activities.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DPV["Principle"]
    class_class_curie: ClassVar[str] = "dpv:Principle"
    class_name: ClassVar[str] = "Principle"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.Principle

    id: Union[str, PrincipleId] = None
    hasDocumentation: Optional[Union[Union[str, DocumentationId], list[Union[str, DocumentationId]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PrincipleId):
            self.id = PrincipleId(self.id)

        if not isinstance(self.hasDocumentation, list):
            self.hasDocumentation = [self.hasDocumentation] if self.hasDocumentation is not None else []
        self.hasDocumentation = [v if isinstance(v, DocumentationId) else DocumentationId(v) for v in self.hasDocumentation]

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class Policy(Entity):
    """
    A guidance document outlining any of: procedures, plans, principles, decisions, intent, or protocols.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DPV["Policy"]
    class_class_curie: ClassVar[str] = "dpv:Policy"
    class_name: ClassVar[str] = "Policy"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.Policy

    id: Union[str, PolicyId] = None
    isDefinedByTaxonomy: Optional[Union[str, TaxonomyId]] = None
    isApplicableinLocality: Optional[Union[Union[str, LocalityOfUseId], list[Union[str, LocalityOfUseId]]]] = empty_list()
    type: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.isDefinedByTaxonomy is not None and not isinstance(self.isDefinedByTaxonomy, TaxonomyId):
            self.isDefinedByTaxonomy = TaxonomyId(self.isDefinedByTaxonomy)

        if not isinstance(self.isApplicableinLocality, list):
            self.isApplicableinLocality = [self.isApplicableinLocality] if self.isApplicableinLocality is not None else []
        self.isApplicableinLocality = [v if isinstance(v, LocalityOfUseId) else LocalityOfUseId(v) for v in self.isApplicableinLocality]

        self.type = str(self.class_name)

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


    def __new__(cls, *args, **kwargs):

        type_designator = "type"
        if not type_designator in kwargs:
            return super().__new__(cls,*args,**kwargs)
        else:
            type_designator_value = kwargs[type_designator]
            target_cls = cls._class_for("class_name", type_designator_value)


            if target_cls is None:
                raise ValueError(f"Wrong type designator value: class {cls.__name__} "
                                 f"has no subclass with ['class_name']='{kwargs[type_designator]}'")
            return super().__new__(target_cls,*args,**kwargs)



@dataclass(repr=False)
class LLMQuestionPolicy(Policy):
    """
    The policy guides how the language model should answer a diverse set of sensitive questions.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["LLMQuestionPolicy"]
    class_class_curie: ClassVar[str] = "nexus:LLMQuestionPolicy"
    class_name: ClassVar[str] = "LLMQuestionPolicy"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.LLMQuestionPolicy

    id: Union[str, LLMQuestionPolicyId] = None
    hasRelatedRisk: Optional[Union[Union[str, RiskId], list[Union[str, RiskId]]]] = empty_list()
    hasRule: Optional[Union[Union[str, RuleId], list[Union[str, RuleId]]]] = empty_list()
    hasReasonDenial: Optional[str] = None
    hasShortReplyType: Optional[str] = None
    hasException: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, LLMQuestionPolicyId):
            self.id = LLMQuestionPolicyId(self.id)

        if not isinstance(self.hasRelatedRisk, list):
            self.hasRelatedRisk = [self.hasRelatedRisk] if self.hasRelatedRisk is not None else []
        self.hasRelatedRisk = [v if isinstance(v, RiskId) else RiskId(v) for v in self.hasRelatedRisk]

        if not isinstance(self.hasRule, list):
            self.hasRule = [self.hasRule] if self.hasRule is not None else []
        self.hasRule = [v if isinstance(v, RuleId) else RuleId(v) for v in self.hasRule]

        if self.hasReasonDenial is not None and not isinstance(self.hasReasonDenial, str):
            self.hasReasonDenial = str(self.hasReasonDenial)

        if self.hasShortReplyType is not None and not isinstance(self.hasShortReplyType, str):
            self.hasShortReplyType = str(self.hasShortReplyType)

        if self.hasException is not None and not isinstance(self.hasException, str):
            self.hasException = str(self.hasException)

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class Rule(Entity):
    """
    A rule describing a process or control that directs or determines if and how an activity should be conducted.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DPV["Rule"]
    class_class_curie: ClassVar[str] = "dpv:Rule"
    class_name: ClassVar[str] = "Rule"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.Rule

    id: Union[str, RuleId] = None
    isDefinedByTaxonomy: Optional[Union[str, TaxonomyId]] = None
    hasRule: Optional[Union[Union[str, RuleId], list[Union[str, RuleId]]]] = empty_list()
    type: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.isDefinedByTaxonomy is not None and not isinstance(self.isDefinedByTaxonomy, TaxonomyId):
            self.isDefinedByTaxonomy = TaxonomyId(self.isDefinedByTaxonomy)

        if not isinstance(self.hasRule, list):
            self.hasRule = [self.hasRule] if self.hasRule is not None else []
        self.hasRule = [v if isinstance(v, RuleId) else RuleId(v) for v in self.hasRule]

        self.type = str(self.class_name)

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


    def __new__(cls, *args, **kwargs):

        type_designator = "type"
        if not type_designator in kwargs:
            return super().__new__(cls,*args,**kwargs)
        else:
            type_designator_value = kwargs[type_designator]
            target_cls = cls._class_for("class_name", type_designator_value)


            if target_cls is None:
                raise ValueError(f"Wrong type designator value: class {cls.__name__} "
                                 f"has no subclass with ['class_name']='{kwargs[type_designator]}'")
            return super().__new__(target_cls,*args,**kwargs)



@dataclass(repr=False)
class AttributeConditionRule(Rule):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["AttributeConditionRule"]
    class_class_curie: ClassVar[str] = "nexus:AttributeConditionRule"
    class_name: ClassVar[str] = "AttributeConditionRule"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.AttributeConditionRule

    id: Union[str, AttributeConditionRuleId] = None
    preconditions: Optional[Union[dict, "AnonymousClassExpression"]] = None
    postconditions: Optional[Union[dict, "AnonymousClassExpression"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AttributeConditionRuleId):
            self.id = AttributeConditionRuleId(self.id)

        if self.preconditions is not None and not isinstance(self.preconditions, AnonymousClassExpression):
            self.preconditions = AnonymousClassExpression(**as_dict(self.preconditions))

        if self.postconditions is not None and not isinstance(self.postconditions, AnonymousClassExpression):
            self.postconditions = AnonymousClassExpression(**as_dict(self.postconditions))

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class AnonymousClassExpression(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["AnonymousClassExpression"]
    class_class_curie: ClassVar[str] = "nexus:AnonymousClassExpression"
    class_name: ClassVar[str] = "AnonymousClassExpression"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.AnonymousClassExpression

    slot_conditions: Optional[Union[Union[dict, "SlotCondition"], list[Union[dict, "SlotCondition"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if not isinstance(self.slot_conditions, list):
            self.slot_conditions = [self.slot_conditions] if self.slot_conditions is not None else []
        self.slot_conditions = [v if isinstance(v, SlotCondition) else SlotCondition(**as_dict(v)) for v in self.slot_conditions]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SlotCondition(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["SlotCondition"]
    class_class_curie: ClassVar[str] = "nexus:SlotCondition"
    class_name: ClassVar[str] = "SlotCondition"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.SlotCondition

    slot_name: Optional[str] = None
    equals_string: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.slot_name is not None and not isinstance(self.slot_name, str):
            self.slot_name = str(self.slot_name)

        if self.equals_string is not None and not isinstance(self.equals_string, str):
            self.equals_string = str(self.equals_string)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Permission(Rule):
    """
    A rule describing a permission to perform an activity
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DPV["Permission"]
    class_class_curie: ClassVar[str] = "dpv:Permission"
    class_name: ClassVar[str] = "Permission"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.Permission

    id: Union[str, PermissionId] = None
    type: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        self.type = str(self.class_name)

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


    def __new__(cls, *args, **kwargs):

        type_designator = "type"
        if not type_designator in kwargs:
            return super().__new__(cls,*args,**kwargs)
        else:
            type_designator_value = kwargs[type_designator]
            target_cls = cls._class_for("class_name", type_designator_value)


            if target_cls is None:
                raise ValueError(f"Wrong type designator value: class {cls.__name__} "
                                 f"has no subclass with ['class_name']='{kwargs[type_designator]}'")
            return super().__new__(target_cls,*args,**kwargs)



@dataclass(repr=False)
class Prohibition(Rule):
    """
    A rule describing a prohibition to perform an activity
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DPV["Prohibition"]
    class_class_curie: ClassVar[str] = "dpv:Prohibition"
    class_name: ClassVar[str] = "Prohibition"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.Prohibition

    id: Union[str, ProhibitionId] = None
    type: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        self.type = str(self.class_name)

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


    def __new__(cls, *args, **kwargs):

        type_designator = "type"
        if not type_designator in kwargs:
            return super().__new__(cls,*args,**kwargs)
        else:
            type_designator_value = kwargs[type_designator]
            target_cls = cls._class_for("class_name", type_designator_value)


            if target_cls is None:
                raise ValueError(f"Wrong type designator value: class {cls.__name__} "
                                 f"has no subclass with ['class_name']='{kwargs[type_designator]}'")
            return super().__new__(target_cls,*args,**kwargs)



@dataclass(repr=False)
class Obligation(Rule):
    """
    A rule describing an obligation for performing an activity
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DPV["Obligation"]
    class_class_curie: ClassVar[str] = "dpv:Obligation"
    class_name: ClassVar[str] = "Obligation"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.Obligation

    id: Union[str, ObligationId] = None
    type: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        self.type = str(self.class_name)

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


    def __new__(cls, *args, **kwargs):

        type_designator = "type"
        if not type_designator in kwargs:
            return super().__new__(cls,*args,**kwargs)
        else:
            type_designator_value = kwargs[type_designator]
            target_cls = cls._class_for("class_name", type_designator_value)


            if target_cls is None:
                raise ValueError(f"Wrong type designator value: class {cls.__name__} "
                                 f"has no subclass with ['class_name']='{kwargs[type_designator]}'")
            return super().__new__(target_cls,*args,**kwargs)



@dataclass(repr=False)
class Recommendation(Rule):
    """
    A rule describing a recommendation for performing an activity
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DPV["Recommendation"]
    class_class_curie: ClassVar[str] = "dpv:Recommendation"
    class_name: ClassVar[str] = "Recommendation"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.Recommendation

    id: Union[str, RecommendationId] = None
    type: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        self.type = str(self.class_name)

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


    def __new__(cls, *args, **kwargs):

        type_designator = "type"
        if not type_designator in kwargs:
            return super().__new__(cls,*args,**kwargs)
        else:
            type_designator_value = kwargs[type_designator]
            target_cls = cls._class_for("class_name", type_designator_value)


            if target_cls is None:
                raise ValueError(f"Wrong type designator value: class {cls.__name__} "
                                 f"has no subclass with ['class_name']='{kwargs[type_designator]}'")
            return super().__new__(target_cls,*args,**kwargs)



@dataclass(repr=False)
class Certification(Entry):
    """
    Certification mechanisms, seals, and marks for the purpose of demonstrating compliance
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DPV["Certification"]
    class_class_curie: ClassVar[str] = "dpv:Certification"
    class_name: ClassVar[str] = "Certification"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.Certification

    id: Union[str, CertificationId] = None
    type: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        self.type = str(self.class_name)

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class RiskTaxonomy(Taxonomy):
    """
    A taxonomy of AI system related risks
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["RiskTaxonomy"]
    class_class_curie: ClassVar[str] = "nexus:RiskTaxonomy"
    class_name: ClassVar[str] = "RiskTaxonomy"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.RiskTaxonomy

    id: Union[str, RiskTaxonomyId] = None
    version: Optional[str] = None
    hasDocumentation: Optional[Union[Union[str, DocumentationId], list[Union[str, DocumentationId]]]] = empty_list()
    hasLicense: Optional[Union[str, LicenseId]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, RiskTaxonomyId):
            self.id = RiskTaxonomyId(self.id)

        if self.version is not None and not isinstance(self.version, str):
            self.version = str(self.version)

        if not isinstance(self.hasDocumentation, list):
            self.hasDocumentation = [self.hasDocumentation] if self.hasDocumentation is not None else []
        self.hasDocumentation = [v if isinstance(v, DocumentationId) else DocumentationId(v) for v in self.hasDocumentation]

        if self.hasLicense is not None and not isinstance(self.hasLicense, LicenseId):
            self.hasLicense = LicenseId(self.hasLicense)

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class RiskControlGroupTaxonomy(Taxonomy):
    """
    A taxonomy of AI system related risk controls groups
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["RiskControlGroupTaxonomy"]
    class_class_curie: ClassVar[str] = "nexus:RiskControlGroupTaxonomy"
    class_name: ClassVar[str] = "RiskControlGroupTaxonomy"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.RiskControlGroupTaxonomy

    id: Union[str, RiskControlGroupTaxonomyId] = None
    version: Optional[str] = None
    hasDocumentation: Optional[Union[Union[str, DocumentationId], list[Union[str, DocumentationId]]]] = empty_list()
    hasLicense: Optional[Union[str, LicenseId]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, RiskControlGroupTaxonomyId):
            self.id = RiskControlGroupTaxonomyId(self.id)

        if self.version is not None and not isinstance(self.version, str):
            self.version = str(self.version)

        if not isinstance(self.hasDocumentation, list):
            self.hasDocumentation = [self.hasDocumentation] if self.hasDocumentation is not None else []
        self.hasDocumentation = [v if isinstance(v, DocumentationId) else DocumentationId(v) for v in self.hasDocumentation]

        if self.hasLicense is not None and not isinstance(self.hasLicense, LicenseId):
            self.hasLicense = LicenseId(self.hasLicense)

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class RiskControlGroup(Group):
    """
    A group of AI system related risk controls.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["RiskControlGroup"]
    class_class_curie: ClassVar[str] = "nexus:RiskControlGroup"
    class_name: ClassVar[str] = "RiskControlGroup"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.RiskControlGroup

    id: Union[str, RiskControlGroupId] = None
    name: Optional[str] = None
    description: Optional[str] = None
    url: Optional[Union[str, URI]] = None
    dateCreated: Optional[Union[str, XSDDate]] = None
    dateModified: Optional[Union[str, XSDDate]] = None
    exact_mappings: Optional[Union[Union[dict, "Any"], list[Union[dict, "Any"]]]] = empty_list()
    close_mappings: Optional[Union[Union[dict, "Any"], list[Union[dict, "Any"]]]] = empty_list()
    related_mappings: Optional[Union[Union[dict, "Any"], list[Union[dict, "Any"]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[dict, "Any"], list[Union[dict, "Any"]]]] = empty_list()
    broad_mappings: Optional[Union[Union[dict, "Any"], list[Union[dict, "Any"]]]] = empty_list()
    isCategorizedAs: Optional[Union[Union[dict, "Any"], list[Union[dict, "Any"]]]] = empty_list()
    hasDocumentation: Optional[Union[Union[str, DocumentationId], list[Union[str, DocumentationId]]]] = empty_list()
    isDefinedByTaxonomy: Optional[Union[str, TaxonomyId]] = None
    hasPart: Optional[Union[Union[str, RiskControlId], list[Union[str, RiskControlId]]]] = empty_list()
    hasJurisdiction: Optional[Union[Union[str, "Jurisdiction"], list[Union[str, "Jurisdiction"]]]] = empty_list()
    isDetectedBy: Optional[Union[Union[str, RiskControlId], list[Union[str, RiskControlId]]]] = empty_list()
    isMitigatedBy: Optional[Union[Union[str, RiskControlId], list[Union[str, RiskControlId]]]] = empty_list()
    isUsedWithinLocality: Optional[Union[Union[str, LocalityOfUseId], list[Union[str, LocalityOfUseId]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, RiskControlGroupId):
            self.id = RiskControlGroupId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.url is not None and not isinstance(self.url, URI):
            self.url = URI(self.url)

        if self.dateCreated is not None and not isinstance(self.dateCreated, XSDDate):
            self.dateCreated = XSDDate(self.dateCreated)

        if self.dateModified is not None and not isinstance(self.dateModified, XSDDate):
            self.dateModified = XSDDate(self.dateModified)

        if not isinstance(self.hasDocumentation, list):
            self.hasDocumentation = [self.hasDocumentation] if self.hasDocumentation is not None else []
        self.hasDocumentation = [v if isinstance(v, DocumentationId) else DocumentationId(v) for v in self.hasDocumentation]

        if self.isDefinedByTaxonomy is not None and not isinstance(self.isDefinedByTaxonomy, TaxonomyId):
            self.isDefinedByTaxonomy = TaxonomyId(self.isDefinedByTaxonomy)

        if not isinstance(self.hasPart, list):
            self.hasPart = [self.hasPart] if self.hasPart is not None else []
        self.hasPart = [v if isinstance(v, RiskControlId) else RiskControlId(v) for v in self.hasPart]

        if not isinstance(self.hasJurisdiction, list):
            self.hasJurisdiction = [self.hasJurisdiction] if self.hasJurisdiction is not None else []
        self.hasJurisdiction = [v if isinstance(v, Jurisdiction) else Jurisdiction(v) for v in self.hasJurisdiction]

        if not isinstance(self.isDetectedBy, list):
            self.isDetectedBy = [self.isDetectedBy] if self.isDetectedBy is not None else []
        self.isDetectedBy = [v if isinstance(v, RiskControlId) else RiskControlId(v) for v in self.isDetectedBy]

        if not isinstance(self.isMitigatedBy, list):
            self.isMitigatedBy = [self.isMitigatedBy] if self.isMitigatedBy is not None else []
        self.isMitigatedBy = [v if isinstance(v, RiskControlId) else RiskControlId(v) for v in self.isMitigatedBy]

        if not isinstance(self.isUsedWithinLocality, list):
            self.isUsedWithinLocality = [self.isUsedWithinLocality] if self.isUsedWithinLocality is not None else []
        self.isUsedWithinLocality = [v if isinstance(v, LocalityOfUseId) else LocalityOfUseId(v) for v in self.isUsedWithinLocality]

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class RiskGroup(Group):
    """
    A group of AI system related risks that are part of a risk taxonomy.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["RiskGroup"]
    class_class_curie: ClassVar[str] = "nexus:RiskGroup"
    class_name: ClassVar[str] = "RiskGroup"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.RiskGroup

    id: Union[str, RiskGroupId] = None
    name: Optional[str] = None
    description: Optional[str] = None
    url: Optional[Union[str, URI]] = None
    dateCreated: Optional[Union[str, XSDDate]] = None
    dateModified: Optional[Union[str, XSDDate]] = None
    exact_mappings: Optional[Union[Union[dict, "Any"], list[Union[dict, "Any"]]]] = empty_list()
    close_mappings: Optional[Union[Union[dict, "Any"], list[Union[dict, "Any"]]]] = empty_list()
    related_mappings: Optional[Union[Union[dict, "Any"], list[Union[dict, "Any"]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[dict, "Any"], list[Union[dict, "Any"]]]] = empty_list()
    broad_mappings: Optional[Union[Union[dict, "Any"], list[Union[dict, "Any"]]]] = empty_list()
    isCategorizedAs: Optional[Union[Union[dict, "Any"], list[Union[dict, "Any"]]]] = empty_list()
    hasDocumentation: Optional[Union[Union[str, DocumentationId], list[Union[str, DocumentationId]]]] = empty_list()
    isDefinedByTaxonomy: Optional[Union[str, TaxonomyId]] = None
    hasPart: Optional[Union[Union[str, RiskId], list[Union[str, RiskId]]]] = empty_list()
    hasJurisdiction: Optional[Union[Union[str, "Jurisdiction"], list[Union[str, "Jurisdiction"]]]] = empty_list()
    isDetectedBy: Optional[Union[Union[str, RiskControlId], list[Union[str, RiskControlId]]]] = empty_list()
    isMitigatedBy: Optional[Union[Union[str, RiskControlId], list[Union[str, RiskControlId]]]] = empty_list()
    isUsedWithinLocality: Optional[Union[Union[str, LocalityOfUseId], list[Union[str, LocalityOfUseId]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, RiskGroupId):
            self.id = RiskGroupId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.url is not None and not isinstance(self.url, URI):
            self.url = URI(self.url)

        if self.dateCreated is not None and not isinstance(self.dateCreated, XSDDate):
            self.dateCreated = XSDDate(self.dateCreated)

        if self.dateModified is not None and not isinstance(self.dateModified, XSDDate):
            self.dateModified = XSDDate(self.dateModified)

        if not isinstance(self.hasDocumentation, list):
            self.hasDocumentation = [self.hasDocumentation] if self.hasDocumentation is not None else []
        self.hasDocumentation = [v if isinstance(v, DocumentationId) else DocumentationId(v) for v in self.hasDocumentation]

        if self.isDefinedByTaxonomy is not None and not isinstance(self.isDefinedByTaxonomy, TaxonomyId):
            self.isDefinedByTaxonomy = TaxonomyId(self.isDefinedByTaxonomy)

        if not isinstance(self.hasPart, list):
            self.hasPart = [self.hasPart] if self.hasPart is not None else []
        self.hasPart = [v if isinstance(v, RiskId) else RiskId(v) for v in self.hasPart]

        if not isinstance(self.hasJurisdiction, list):
            self.hasJurisdiction = [self.hasJurisdiction] if self.hasJurisdiction is not None else []
        self.hasJurisdiction = [v if isinstance(v, Jurisdiction) else Jurisdiction(v) for v in self.hasJurisdiction]

        if not isinstance(self.isDetectedBy, list):
            self.isDetectedBy = [self.isDetectedBy] if self.isDetectedBy is not None else []
        self.isDetectedBy = [v if isinstance(v, RiskControlId) else RiskControlId(v) for v in self.isDetectedBy]

        if not isinstance(self.isMitigatedBy, list):
            self.isMitigatedBy = [self.isMitigatedBy] if self.isMitigatedBy is not None else []
        self.isMitigatedBy = [v if isinstance(v, RiskControlId) else RiskControlId(v) for v in self.isMitigatedBy]

        if not isinstance(self.isUsedWithinLocality, list):
            self.isUsedWithinLocality = [self.isUsedWithinLocality] if self.isUsedWithinLocality is not None else []
        self.isUsedWithinLocality = [v if isinstance(v, LocalityOfUseId) else LocalityOfUseId(v) for v in self.isUsedWithinLocality]

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class Risk(Entry):
    """
    The state of uncertainty associated with an AI system, that has the potential to cause harms
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AIRO["Risk"]
    class_class_curie: ClassVar[str] = "airo:Risk"
    class_name: ClassVar[str] = "Risk"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.Risk

    id: Union[str, RiskId] = None
    name: Optional[str] = None
    description: Optional[str] = None
    url: Optional[Union[str, URI]] = None
    dateCreated: Optional[Union[str, XSDDate]] = None
    dateModified: Optional[Union[str, XSDDate]] = None
    exact_mappings: Optional[Union[Union[dict, "Any"], list[Union[dict, "Any"]]]] = empty_list()
    close_mappings: Optional[Union[Union[dict, "Any"], list[Union[dict, "Any"]]]] = empty_list()
    related_mappings: Optional[Union[Union[dict, "Any"], list[Union[dict, "Any"]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[dict, "Any"], list[Union[dict, "Any"]]]] = empty_list()
    broad_mappings: Optional[Union[Union[dict, "Any"], list[Union[dict, "Any"]]]] = empty_list()
    isCategorizedAs: Optional[Union[Union[dict, "Any"], list[Union[dict, "Any"]]]] = empty_list()
    hasDocumentation: Optional[Union[Union[str, DocumentationId], list[Union[str, DocumentationId]]]] = empty_list()
    hasRelatedAction: Optional[Union[Union[str, ActionId], list[Union[str, ActionId]]]] = empty_list()
    isDefinedByTaxonomy: Optional[Union[str, TaxonomyId]] = None
    isPartOf: Optional[Union[str, RiskGroupId]] = None
    detectsRiskConcept: Optional[Union[Union[str, RiskConceptId], list[Union[str, RiskConceptId]]]] = empty_list()
    tag: Optional[str] = None
    risk_type: Optional[str] = None
    phase: Optional[str] = None
    descriptor: Optional[Union[str, list[str]]] = empty_list()
    concern: Optional[str] = None
    hasJurisdiction: Optional[Union[Union[str, "Jurisdiction"], list[Union[str, "Jurisdiction"]]]] = empty_list()
    isDetectedBy: Optional[Union[Union[str, RiskControlId], list[Union[str, RiskControlId]]]] = empty_list()
    isMitigatedBy: Optional[Union[Union[str, RiskControlId], list[Union[str, RiskControlId]]]] = empty_list()
    isUsedWithinLocality: Optional[Union[Union[str, LocalityOfUseId], list[Union[str, LocalityOfUseId]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, RiskId):
            self.id = RiskId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.url is not None and not isinstance(self.url, URI):
            self.url = URI(self.url)

        if self.dateCreated is not None and not isinstance(self.dateCreated, XSDDate):
            self.dateCreated = XSDDate(self.dateCreated)

        if self.dateModified is not None and not isinstance(self.dateModified, XSDDate):
            self.dateModified = XSDDate(self.dateModified)

        if not isinstance(self.hasDocumentation, list):
            self.hasDocumentation = [self.hasDocumentation] if self.hasDocumentation is not None else []
        self.hasDocumentation = [v if isinstance(v, DocumentationId) else DocumentationId(v) for v in self.hasDocumentation]

        if not isinstance(self.hasRelatedAction, list):
            self.hasRelatedAction = [self.hasRelatedAction] if self.hasRelatedAction is not None else []
        self.hasRelatedAction = [v if isinstance(v, ActionId) else ActionId(v) for v in self.hasRelatedAction]

        if self.isDefinedByTaxonomy is not None and not isinstance(self.isDefinedByTaxonomy, TaxonomyId):
            self.isDefinedByTaxonomy = TaxonomyId(self.isDefinedByTaxonomy)

        if self.isPartOf is not None and not isinstance(self.isPartOf, RiskGroupId):
            self.isPartOf = RiskGroupId(self.isPartOf)

        if not isinstance(self.detectsRiskConcept, list):
            self.detectsRiskConcept = [self.detectsRiskConcept] if self.detectsRiskConcept is not None else []
        self.detectsRiskConcept = [v if isinstance(v, RiskConceptId) else RiskConceptId(v) for v in self.detectsRiskConcept]

        if self.tag is not None and not isinstance(self.tag, str):
            self.tag = str(self.tag)

        if self.risk_type is not None and not isinstance(self.risk_type, str):
            self.risk_type = str(self.risk_type)

        if self.phase is not None and not isinstance(self.phase, str):
            self.phase = str(self.phase)

        if not isinstance(self.descriptor, list):
            self.descriptor = [self.descriptor] if self.descriptor is not None else []
        self.descriptor = [v if isinstance(v, str) else str(v) for v in self.descriptor]

        if self.concern is not None and not isinstance(self.concern, str):
            self.concern = str(self.concern)

        if not isinstance(self.hasJurisdiction, list):
            self.hasJurisdiction = [self.hasJurisdiction] if self.hasJurisdiction is not None else []
        self.hasJurisdiction = [v if isinstance(v, Jurisdiction) else Jurisdiction(v) for v in self.hasJurisdiction]

        if not isinstance(self.isDetectedBy, list):
            self.isDetectedBy = [self.isDetectedBy] if self.isDetectedBy is not None else []
        self.isDetectedBy = [v if isinstance(v, RiskControlId) else RiskControlId(v) for v in self.isDetectedBy]

        if not isinstance(self.isMitigatedBy, list):
            self.isMitigatedBy = [self.isMitigatedBy] if self.isMitigatedBy is not None else []
        self.isMitigatedBy = [v if isinstance(v, RiskControlId) else RiskControlId(v) for v in self.isMitigatedBy]

        if not isinstance(self.isUsedWithinLocality, list):
            self.isUsedWithinLocality = [self.isUsedWithinLocality] if self.isUsedWithinLocality is not None else []
        self.isUsedWithinLocality = [v if isinstance(v, LocalityOfUseId) else LocalityOfUseId(v) for v in self.isUsedWithinLocality]

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class RiskConcept(Concept):
    """
    An umbrella term for referring to risk, risk source, consequence and impact.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AIRO["RiskConcept"]
    class_class_curie: ClassVar[str] = "airo:RiskConcept"
    class_name: ClassVar[str] = "RiskConcept"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.RiskConcept

    id: Union[str, RiskConceptId] = None
    isDetectedBy: Optional[Union[Union[str, RiskControlId], list[Union[str, RiskControlId]]]] = empty_list()
    isMitigatedBy: Optional[Union[Union[str, RiskControlId], list[Union[str, RiskControlId]]]] = empty_list()
    isUsedWithinLocality: Optional[Union[Union[str, LocalityOfUseId], list[Union[str, LocalityOfUseId]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if not isinstance(self.isDetectedBy, list):
            self.isDetectedBy = [self.isDetectedBy] if self.isDetectedBy is not None else []
        self.isDetectedBy = [v if isinstance(v, RiskControlId) else RiskControlId(v) for v in self.isDetectedBy]

        if not isinstance(self.isMitigatedBy, list):
            self.isMitigatedBy = [self.isMitigatedBy] if self.isMitigatedBy is not None else []
        self.isMitigatedBy = [v if isinstance(v, RiskControlId) else RiskControlId(v) for v in self.isMitigatedBy]

        if not isinstance(self.isUsedWithinLocality, list):
            self.isUsedWithinLocality = [self.isUsedWithinLocality] if self.isUsedWithinLocality is not None else []
        self.isUsedWithinLocality = [v if isinstance(v, LocalityOfUseId) else LocalityOfUseId(v) for v in self.isUsedWithinLocality]

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class RiskControl(Control):
    """
    A measure that maintains and/or modifies risk (and risk concepts)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AIRO["RiskControl"]
    class_class_curie: ClassVar[str] = "airo:RiskControl"
    class_name: ClassVar[str] = "RiskControl"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.RiskControl

    id: Union[str, RiskControlId] = None
    name: Optional[str] = None
    description: Optional[str] = None
    url: Optional[Union[str, URI]] = None
    dateCreated: Optional[Union[str, XSDDate]] = None
    dateModified: Optional[Union[str, XSDDate]] = None
    exact_mappings: Optional[Union[Union[dict, "Any"], list[Union[dict, "Any"]]]] = empty_list()
    close_mappings: Optional[Union[Union[dict, "Any"], list[Union[dict, "Any"]]]] = empty_list()
    related_mappings: Optional[Union[Union[dict, "Any"], list[Union[dict, "Any"]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[dict, "Any"], list[Union[dict, "Any"]]]] = empty_list()
    broad_mappings: Optional[Union[Union[dict, "Any"], list[Union[dict, "Any"]]]] = empty_list()
    isCategorizedAs: Optional[Union[Union[dict, "Any"], list[Union[dict, "Any"]]]] = empty_list()
    detectsRiskConcept: Optional[Union[Union[str, RiskConceptId], list[Union[str, RiskConceptId]]]] = empty_list()
    mitigatesRiskConcept: Optional[Union[Union[str, RiskConceptId], list[Union[str, RiskConceptId]]]] = empty_list()
    isDefinedByTaxonomy: Optional[Union[str, TaxonomyId]] = None
    hasDocumentation: Optional[Union[Union[str, DocumentationId], list[Union[str, DocumentationId]]]] = empty_list()
    hasJurisdiction: Optional[Union[Union[str, "Jurisdiction"], list[Union[str, "Jurisdiction"]]]] = empty_list()
    isDetectedBy: Optional[Union[Union[str, RiskControlId], list[Union[str, RiskControlId]]]] = empty_list()
    isMitigatedBy: Optional[Union[Union[str, RiskControlId], list[Union[str, RiskControlId]]]] = empty_list()
    isUsedWithinLocality: Optional[Union[Union[str, LocalityOfUseId], list[Union[str, LocalityOfUseId]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, RiskControlId):
            self.id = RiskControlId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.url is not None and not isinstance(self.url, URI):
            self.url = URI(self.url)

        if self.dateCreated is not None and not isinstance(self.dateCreated, XSDDate):
            self.dateCreated = XSDDate(self.dateCreated)

        if self.dateModified is not None and not isinstance(self.dateModified, XSDDate):
            self.dateModified = XSDDate(self.dateModified)

        if not isinstance(self.detectsRiskConcept, list):
            self.detectsRiskConcept = [self.detectsRiskConcept] if self.detectsRiskConcept is not None else []
        self.detectsRiskConcept = [v if isinstance(v, RiskConceptId) else RiskConceptId(v) for v in self.detectsRiskConcept]

        if not isinstance(self.mitigatesRiskConcept, list):
            self.mitigatesRiskConcept = [self.mitigatesRiskConcept] if self.mitigatesRiskConcept is not None else []
        self.mitigatesRiskConcept = [v if isinstance(v, RiskConceptId) else RiskConceptId(v) for v in self.mitigatesRiskConcept]

        if self.isDefinedByTaxonomy is not None and not isinstance(self.isDefinedByTaxonomy, TaxonomyId):
            self.isDefinedByTaxonomy = TaxonomyId(self.isDefinedByTaxonomy)

        if not isinstance(self.hasDocumentation, list):
            self.hasDocumentation = [self.hasDocumentation] if self.hasDocumentation is not None else []
        self.hasDocumentation = [v if isinstance(v, DocumentationId) else DocumentationId(v) for v in self.hasDocumentation]

        if not isinstance(self.hasJurisdiction, list):
            self.hasJurisdiction = [self.hasJurisdiction] if self.hasJurisdiction is not None else []
        self.hasJurisdiction = [v if isinstance(v, Jurisdiction) else Jurisdiction(v) for v in self.hasJurisdiction]

        if not isinstance(self.isDetectedBy, list):
            self.isDetectedBy = [self.isDetectedBy] if self.isDetectedBy is not None else []
        self.isDetectedBy = [v if isinstance(v, RiskControlId) else RiskControlId(v) for v in self.isDetectedBy]

        if not isinstance(self.isMitigatedBy, list):
            self.isMitigatedBy = [self.isMitigatedBy] if self.isMitigatedBy is not None else []
        self.isMitigatedBy = [v if isinstance(v, RiskControlId) else RiskControlId(v) for v in self.isMitigatedBy]

        if not isinstance(self.isUsedWithinLocality, list):
            self.isUsedWithinLocality = [self.isUsedWithinLocality] if self.isUsedWithinLocality is not None else []
        self.isUsedWithinLocality = [v if isinstance(v, LocalityOfUseId) else LocalityOfUseId(v) for v in self.isUsedWithinLocality]

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class Action(RiskControl):
    """
    Action to remediate a risk
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["Action"]
    class_class_curie: ClassVar[str] = "nexus:Action"
    class_name: ClassVar[str] = "Action"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.Action

    id: Union[str, ActionId] = None
    hasRelatedRisk: Optional[Union[Union[str, RiskId], list[Union[str, RiskId]]]] = empty_list()
    hasDocumentation: Optional[Union[Union[str, DocumentationId], list[Union[str, DocumentationId]]]] = empty_list()
    isDefinedByTaxonomy: Optional[Union[str, TaxonomyId]] = None
    hasAiActorTask: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ActionId):
            self.id = ActionId(self.id)

        if not isinstance(self.hasRelatedRisk, list):
            self.hasRelatedRisk = [self.hasRelatedRisk] if self.hasRelatedRisk is not None else []
        self.hasRelatedRisk = [v if isinstance(v, RiskId) else RiskId(v) for v in self.hasRelatedRisk]

        if not isinstance(self.hasDocumentation, list):
            self.hasDocumentation = [self.hasDocumentation] if self.hasDocumentation is not None else []
        self.hasDocumentation = [v if isinstance(v, DocumentationId) else DocumentationId(v) for v in self.hasDocumentation]

        if self.isDefinedByTaxonomy is not None and not isinstance(self.isDefinedByTaxonomy, TaxonomyId):
            self.isDefinedByTaxonomy = TaxonomyId(self.isDefinedByTaxonomy)

        if not isinstance(self.hasAiActorTask, list):
            self.hasAiActorTask = [self.hasAiActorTask] if self.hasAiActorTask is not None else []
        self.hasAiActorTask = [v if isinstance(v, str) else str(v) for v in self.hasAiActorTask]

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


Any = Any

@dataclass(repr=False)
class RiskIncident(Entity):
    """
    An event occuring or occured which is a realised or materialised risk.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DPV_RISK["Incident"]
    class_class_curie: ClassVar[str] = "dpv_risk:Incident"
    class_name: ClassVar[str] = "RiskIncident"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.RiskIncident

    id: Union[str, RiskIncidentId] = None
    name: Optional[str] = None
    description: Optional[str] = None
    url: Optional[Union[str, URI]] = None
    dateCreated: Optional[Union[str, XSDDate]] = None
    dateModified: Optional[Union[str, XSDDate]] = None
    exact_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    close_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    related_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    broad_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    isCategorizedAs: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    refersToRisk: Optional[Union[Union[str, RiskId], list[Union[str, RiskId]]]] = empty_list()
    isDefinedByTaxonomy: Optional[Union[str, TaxonomyId]] = None
    hasStatus: Optional[Union[str, IncidentStatusId]] = None
    hasSeverity: Optional[Union[str, SeverityId]] = None
    hasLikelihood: Optional[Union[str, LikelihoodId]] = None
    hasImpactOn: Optional[Union[str, ImpactId]] = None
    hasConsequence: Optional[Union[str, ConsequenceId]] = None
    hasImpact: Optional[Union[str, ImpactId]] = None
    hasVariant: Optional[Union[str, RiskIncidentId]] = None
    author: Optional[str] = None
    source_uri: Optional[str] = None
    hasDocumentation: Optional[Union[Union[str, DocumentationId], list[Union[str, DocumentationId]]]] = empty_list()
    hasJurisdiction: Optional[Union[Union[str, "Jurisdiction"], list[Union[str, "Jurisdiction"]]]] = empty_list()
    type: Optional[str] = None
    isDetectedBy: Optional[Union[Union[str, RiskControlId], list[Union[str, RiskControlId]]]] = empty_list()
    isMitigatedBy: Optional[Union[Union[str, RiskControlId], list[Union[str, RiskControlId]]]] = empty_list()
    isUsedWithinLocality: Optional[Union[Union[str, LocalityOfUseId], list[Union[str, LocalityOfUseId]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, RiskIncidentId):
            self.id = RiskIncidentId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.url is not None and not isinstance(self.url, URI):
            self.url = URI(self.url)

        if self.dateCreated is not None and not isinstance(self.dateCreated, XSDDate):
            self.dateCreated = XSDDate(self.dateCreated)

        if self.dateModified is not None and not isinstance(self.dateModified, XSDDate):
            self.dateModified = XSDDate(self.dateModified)

        if not isinstance(self.refersToRisk, list):
            self.refersToRisk = [self.refersToRisk] if self.refersToRisk is not None else []
        self.refersToRisk = [v if isinstance(v, RiskId) else RiskId(v) for v in self.refersToRisk]

        if self.isDefinedByTaxonomy is not None and not isinstance(self.isDefinedByTaxonomy, TaxonomyId):
            self.isDefinedByTaxonomy = TaxonomyId(self.isDefinedByTaxonomy)

        if self.hasStatus is not None and not isinstance(self.hasStatus, IncidentStatusId):
            self.hasStatus = IncidentStatusId(self.hasStatus)

        if self.hasSeverity is not None and not isinstance(self.hasSeverity, SeverityId):
            self.hasSeverity = SeverityId(self.hasSeverity)

        if self.hasLikelihood is not None and not isinstance(self.hasLikelihood, LikelihoodId):
            self.hasLikelihood = LikelihoodId(self.hasLikelihood)

        if self.hasImpactOn is not None and not isinstance(self.hasImpactOn, ImpactId):
            self.hasImpactOn = ImpactId(self.hasImpactOn)

        if self.hasConsequence is not None and not isinstance(self.hasConsequence, ConsequenceId):
            self.hasConsequence = ConsequenceId(self.hasConsequence)

        if self.hasImpact is not None and not isinstance(self.hasImpact, ImpactId):
            self.hasImpact = ImpactId(self.hasImpact)

        if self.hasVariant is not None and not isinstance(self.hasVariant, RiskIncidentId):
            self.hasVariant = RiskIncidentId(self.hasVariant)

        if self.author is not None and not isinstance(self.author, str):
            self.author = str(self.author)

        if self.source_uri is not None and not isinstance(self.source_uri, str):
            self.source_uri = str(self.source_uri)

        if not isinstance(self.hasDocumentation, list):
            self.hasDocumentation = [self.hasDocumentation] if self.hasDocumentation is not None else []
        self.hasDocumentation = [v if isinstance(v, DocumentationId) else DocumentationId(v) for v in self.hasDocumentation]

        if not isinstance(self.hasJurisdiction, list):
            self.hasJurisdiction = [self.hasJurisdiction] if self.hasJurisdiction is not None else []
        self.hasJurisdiction = [v if isinstance(v, Jurisdiction) else Jurisdiction(v) for v in self.hasJurisdiction]

        self.type = str(self.class_name)

        if not isinstance(self.isDetectedBy, list):
            self.isDetectedBy = [self.isDetectedBy] if self.isDetectedBy is not None else []
        self.isDetectedBy = [v if isinstance(v, RiskControlId) else RiskControlId(v) for v in self.isDetectedBy]

        if not isinstance(self.isMitigatedBy, list):
            self.isMitigatedBy = [self.isMitigatedBy] if self.isMitigatedBy is not None else []
        self.isMitigatedBy = [v if isinstance(v, RiskControlId) else RiskControlId(v) for v in self.isMitigatedBy]

        if not isinstance(self.isUsedWithinLocality, list):
            self.isUsedWithinLocality = [self.isUsedWithinLocality] if self.isUsedWithinLocality is not None else []
        self.isUsedWithinLocality = [v if isinstance(v, LocalityOfUseId) else LocalityOfUseId(v) for v in self.isUsedWithinLocality]

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class Impact(Entity):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DPV["Impact"]
    class_class_curie: ClassVar[str] = "dpv:Impact"
    class_name: ClassVar[str] = "Impact"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.Impact

    id: Union[str, ImpactId] = None
    name: Optional[str] = None
    description: Optional[str] = None
    url: Optional[Union[str, URI]] = None
    dateCreated: Optional[Union[str, XSDDate]] = None
    dateModified: Optional[Union[str, XSDDate]] = None
    exact_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    close_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    related_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    broad_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    isCategorizedAs: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    isDefinedByTaxonomy: Optional[Union[str, TaxonomyId]] = None
    hasDocumentation: Optional[Union[Union[str, DocumentationId], list[Union[str, DocumentationId]]]] = empty_list()
    hasJurisdiction: Optional[Union[Union[str, "Jurisdiction"], list[Union[str, "Jurisdiction"]]]] = empty_list()
    type: Optional[str] = None
    isDetectedBy: Optional[Union[Union[str, RiskControlId], list[Union[str, RiskControlId]]]] = empty_list()
    isMitigatedBy: Optional[Union[Union[str, RiskControlId], list[Union[str, RiskControlId]]]] = empty_list()
    isUsedWithinLocality: Optional[Union[Union[str, LocalityOfUseId], list[Union[str, LocalityOfUseId]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ImpactId):
            self.id = ImpactId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.url is not None and not isinstance(self.url, URI):
            self.url = URI(self.url)

        if self.dateCreated is not None and not isinstance(self.dateCreated, XSDDate):
            self.dateCreated = XSDDate(self.dateCreated)

        if self.dateModified is not None and not isinstance(self.dateModified, XSDDate):
            self.dateModified = XSDDate(self.dateModified)

        if self.isDefinedByTaxonomy is not None and not isinstance(self.isDefinedByTaxonomy, TaxonomyId):
            self.isDefinedByTaxonomy = TaxonomyId(self.isDefinedByTaxonomy)

        if not isinstance(self.hasDocumentation, list):
            self.hasDocumentation = [self.hasDocumentation] if self.hasDocumentation is not None else []
        self.hasDocumentation = [v if isinstance(v, DocumentationId) else DocumentationId(v) for v in self.hasDocumentation]

        if not isinstance(self.hasJurisdiction, list):
            self.hasJurisdiction = [self.hasJurisdiction] if self.hasJurisdiction is not None else []
        self.hasJurisdiction = [v if isinstance(v, Jurisdiction) else Jurisdiction(v) for v in self.hasJurisdiction]

        self.type = str(self.class_name)

        if not isinstance(self.isDetectedBy, list):
            self.isDetectedBy = [self.isDetectedBy] if self.isDetectedBy is not None else []
        self.isDetectedBy = [v if isinstance(v, RiskControlId) else RiskControlId(v) for v in self.isDetectedBy]

        if not isinstance(self.isMitigatedBy, list):
            self.isMitigatedBy = [self.isMitigatedBy] if self.isMitigatedBy is not None else []
        self.isMitigatedBy = [v if isinstance(v, RiskControlId) else RiskControlId(v) for v in self.isMitigatedBy]

        if not isinstance(self.isUsedWithinLocality, list):
            self.isUsedWithinLocality = [self.isUsedWithinLocality] if self.isUsedWithinLocality is not None else []
        self.isUsedWithinLocality = [v if isinstance(v, LocalityOfUseId) else LocalityOfUseId(v) for v in self.isUsedWithinLocality]

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class IncidentStatus(Entity):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DPV["IncidentStatus"]
    class_class_curie: ClassVar[str] = "dpv:IncidentStatus"
    class_name: ClassVar[str] = "IncidentStatus"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.IncidentStatus

    id: Union[str, IncidentStatusId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, IncidentStatusId):
            self.id = IncidentStatusId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class IncidentConcludedclass(IncidentStatus):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DPV["IncidentConcludedclass"]
    class_class_curie: ClassVar[str] = "dpv:IncidentConcludedclass"
    class_name: ClassVar[str] = "IncidentConcludedclass"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.IncidentConcludedclass

    id: Union[str, IncidentConcludedclassId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, IncidentConcludedclassId):
            self.id = IncidentConcludedclassId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class IncidentHaltedclass(IncidentStatus):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DPV["IncidentHaltedclass"]
    class_class_curie: ClassVar[str] = "dpv:IncidentHaltedclass"
    class_name: ClassVar[str] = "IncidentHaltedclass"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.IncidentHaltedclass

    id: Union[str, IncidentHaltedclassId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, IncidentHaltedclassId):
            self.id = IncidentHaltedclassId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class IncidentMitigatedclass(IncidentStatus):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DPV["IncidentMitigatedclass"]
    class_class_curie: ClassVar[str] = "dpv:IncidentMitigatedclass"
    class_name: ClassVar[str] = "IncidentMitigatedclass"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.IncidentMitigatedclass

    id: Union[str, IncidentMitigatedclassId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, IncidentMitigatedclassId):
            self.id = IncidentMitigatedclassId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class IncidentNearMissclass(IncidentStatus):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DPV["IncidentNearMissclass"]
    class_class_curie: ClassVar[str] = "dpv:IncidentNearMissclass"
    class_name: ClassVar[str] = "IncidentNearMissclass"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.IncidentNearMissclass

    id: Union[str, IncidentNearMissclassId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, IncidentNearMissclassId):
            self.id = IncidentNearMissclassId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class IncidentOngoingclass(IncidentStatus):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DPV["IncidentOngoingclass"]
    class_class_curie: ClassVar[str] = "dpv:IncidentOngoingclass"
    class_name: ClassVar[str] = "IncidentOngoingclass"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.IncidentOngoingclass

    id: Union[str, IncidentOngoingclassId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, IncidentOngoingclassId):
            self.id = IncidentOngoingclassId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Severity(Entity):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DPV["Severity"]
    class_class_curie: ClassVar[str] = "dpv:Severity"
    class_name: ClassVar[str] = "Severity"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.Severity

    id: Union[str, SeverityId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, SeverityId):
            self.id = SeverityId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Likelihood(Entity):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DPV["Likelihood"]
    class_class_curie: ClassVar[str] = "dpv:Likelihood"
    class_name: ClassVar[str] = "Likelihood"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.Likelihood

    id: Union[str, LikelihoodId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, LikelihoodId):
            self.id = LikelihoodId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Consequence(Entity):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DPV["Consequence"]
    class_class_curie: ClassVar[str] = "dpv:Consequence"
    class_name: ClassVar[str] = "Consequence"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.Consequence

    id: Union[str, ConsequenceId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ConsequenceId):
            self.id = ConsequenceId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class CapabilityTaxonomy(Taxonomy):
    """
    A taxonomy of AI capabilities describing the abilities of AI systems.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SKOS["ConceptScheme"]
    class_class_curie: ClassVar[str] = "skos:ConceptScheme"
    class_name: ClassVar[str] = "CapabilityTaxonomy"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.CapabilityTaxonomy

    id: Union[str, CapabilityTaxonomyId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, CapabilityTaxonomyId):
            self.id = CapabilityTaxonomyId(self.id)

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class CapabilityConcept(Concept):
    """
    An umbrella term for referring to capability domains, groups, and individual capabilities.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["CapabilityConcept"]
    class_class_curie: ClassVar[str] = "nexus:CapabilityConcept"
    class_name: ClassVar[str] = "CapabilityConcept"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.CapabilityConcept

    id: Union[str, CapabilityConceptId] = None

    def __post_init__(self, *_: str, **kwargs: Any):

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class CapabilityDomain(Group):
    """
    A high-level domain of AI capabilities (e.g., Language, Reasoning, Knowledge)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["CapabilityDomain"]
    class_class_curie: ClassVar[str] = "nexus:CapabilityDomain"
    class_name: ClassVar[str] = "CapabilityDomain"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.CapabilityDomain

    id: Union[str, CapabilityDomainId] = None
    name: Optional[str] = None
    description: Optional[str] = None
    url: Optional[Union[str, URI]] = None
    dateCreated: Optional[Union[str, XSDDate]] = None
    dateModified: Optional[Union[str, XSDDate]] = None
    exact_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    close_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    related_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    broad_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    isCategorizedAs: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    isDefinedByTaxonomy: Optional[Union[str, TaxonomyId]] = None
    hasDocumentation: Optional[Union[Union[str, DocumentationId], list[Union[str, DocumentationId]]]] = empty_list()
    hasPart: Optional[Union[Union[str, CapabilityGroupId], list[Union[str, CapabilityGroupId]]]] = empty_list()
    hasJurisdiction: Optional[Union[Union[str, "Jurisdiction"], list[Union[str, "Jurisdiction"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, CapabilityDomainId):
            self.id = CapabilityDomainId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.url is not None and not isinstance(self.url, URI):
            self.url = URI(self.url)

        if self.dateCreated is not None and not isinstance(self.dateCreated, XSDDate):
            self.dateCreated = XSDDate(self.dateCreated)

        if self.dateModified is not None and not isinstance(self.dateModified, XSDDate):
            self.dateModified = XSDDate(self.dateModified)

        if self.isDefinedByTaxonomy is not None and not isinstance(self.isDefinedByTaxonomy, TaxonomyId):
            self.isDefinedByTaxonomy = TaxonomyId(self.isDefinedByTaxonomy)

        if not isinstance(self.hasDocumentation, list):
            self.hasDocumentation = [self.hasDocumentation] if self.hasDocumentation is not None else []
        self.hasDocumentation = [v if isinstance(v, DocumentationId) else DocumentationId(v) for v in self.hasDocumentation]

        if not isinstance(self.hasPart, list):
            self.hasPart = [self.hasPart] if self.hasPart is not None else []
        self.hasPart = [v if isinstance(v, CapabilityGroupId) else CapabilityGroupId(v) for v in self.hasPart]

        if not isinstance(self.hasJurisdiction, list):
            self.hasJurisdiction = [self.hasJurisdiction] if self.hasJurisdiction is not None else []
        self.hasJurisdiction = [v if isinstance(v, Jurisdiction) else Jurisdiction(v) for v in self.hasJurisdiction]

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class CapabilityGroup(Group):
    """
    A group of AI capabilities that are part of a capability taxonomy, organized under a domain
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["CapabilityGroup"]
    class_class_curie: ClassVar[str] = "nexus:CapabilityGroup"
    class_name: ClassVar[str] = "CapabilityGroup"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.CapabilityGroup

    id: Union[str, CapabilityGroupId] = None
    name: Optional[str] = None
    description: Optional[str] = None
    url: Optional[Union[str, URI]] = None
    dateCreated: Optional[Union[str, XSDDate]] = None
    dateModified: Optional[Union[str, XSDDate]] = None
    exact_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    close_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    related_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    broad_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    isCategorizedAs: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    hasDocumentation: Optional[Union[Union[str, DocumentationId], list[Union[str, DocumentationId]]]] = empty_list()
    isDefinedByTaxonomy: Optional[Union[str, TaxonomyId]] = None
    isPartOf: Optional[Union[str, CapabilityDomainId]] = None
    hasPart: Optional[Union[Union[str, CapabilityId], list[Union[str, CapabilityId]]]] = empty_list()
    belongsToDomain: Optional[Union[str, CapabilityDomainId]] = None
    hasJurisdiction: Optional[Union[Union[str, "Jurisdiction"], list[Union[str, "Jurisdiction"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, CapabilityGroupId):
            self.id = CapabilityGroupId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.url is not None and not isinstance(self.url, URI):
            self.url = URI(self.url)

        if self.dateCreated is not None and not isinstance(self.dateCreated, XSDDate):
            self.dateCreated = XSDDate(self.dateCreated)

        if self.dateModified is not None and not isinstance(self.dateModified, XSDDate):
            self.dateModified = XSDDate(self.dateModified)

        if not isinstance(self.hasDocumentation, list):
            self.hasDocumentation = [self.hasDocumentation] if self.hasDocumentation is not None else []
        self.hasDocumentation = [v if isinstance(v, DocumentationId) else DocumentationId(v) for v in self.hasDocumentation]

        if self.isDefinedByTaxonomy is not None and not isinstance(self.isDefinedByTaxonomy, TaxonomyId):
            self.isDefinedByTaxonomy = TaxonomyId(self.isDefinedByTaxonomy)

        if self.isPartOf is not None and not isinstance(self.isPartOf, CapabilityDomainId):
            self.isPartOf = CapabilityDomainId(self.isPartOf)

        if not isinstance(self.hasPart, list):
            self.hasPart = [self.hasPart] if self.hasPart is not None else []
        self.hasPart = [v if isinstance(v, CapabilityId) else CapabilityId(v) for v in self.hasPart]

        if self.belongsToDomain is not None and not isinstance(self.belongsToDomain, CapabilityDomainId):
            self.belongsToDomain = CapabilityDomainId(self.belongsToDomain)

        if not isinstance(self.hasJurisdiction, list):
            self.hasJurisdiction = [self.hasJurisdiction] if self.hasJurisdiction is not None else []
        self.hasJurisdiction = [v if isinstance(v, Jurisdiction) else Jurisdiction(v) for v in self.hasJurisdiction]

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class Capability(Entry):
    """
    A specific AI capability or ability, such as reading comprehension, logical reasoning, or code generation. Aligned
    with the W3C DPV AI extension dpv-ai:Capability, representing what an AI technology is capable of achieving or
    providing.
    Capabilities are distinct from: (1) the intended purpose for which the technology is designed, (2) the actual
    tasks performed in a specific deployment context, and (3) the technical implementation mechanisms (intrinsics,
    adapters) that enable the capability.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AI["Capability"]
    class_class_curie: ClassVar[str] = "ai:Capability"
    class_name: ClassVar[str] = "Capability"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.Capability

    id: Union[str, CapabilityId] = None
    name: Optional[str] = None
    description: Optional[str] = None
    url: Optional[Union[str, URI]] = None
    dateCreated: Optional[Union[str, XSDDate]] = None
    dateModified: Optional[Union[str, XSDDate]] = None
    exact_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    close_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    related_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    broad_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    isCategorizedAs: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    isDefinedByTaxonomy: Optional[Union[str, TaxonomyId]] = None
    hasDocumentation: Optional[Union[Union[str, DocumentationId], list[Union[str, DocumentationId]]]] = empty_list()
    requiredByTask: Optional[Union[Union[str, AiTaskId], list[Union[str, AiTaskId]]]] = empty_list()
    implementedByAdapter: Optional[Union[Union[str, AdapterId], list[Union[str, AdapterId]]]] = empty_list()
    isPartOf: Optional[Union[str, CapabilityGroupId]] = None
    hasJurisdiction: Optional[Union[Union[str, "Jurisdiction"], list[Union[str, "Jurisdiction"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, CapabilityId):
            self.id = CapabilityId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.url is not None and not isinstance(self.url, URI):
            self.url = URI(self.url)

        if self.dateCreated is not None and not isinstance(self.dateCreated, XSDDate):
            self.dateCreated = XSDDate(self.dateCreated)

        if self.dateModified is not None and not isinstance(self.dateModified, XSDDate):
            self.dateModified = XSDDate(self.dateModified)

        if self.isDefinedByTaxonomy is not None and not isinstance(self.isDefinedByTaxonomy, TaxonomyId):
            self.isDefinedByTaxonomy = TaxonomyId(self.isDefinedByTaxonomy)

        if not isinstance(self.hasDocumentation, list):
            self.hasDocumentation = [self.hasDocumentation] if self.hasDocumentation is not None else []
        self.hasDocumentation = [v if isinstance(v, DocumentationId) else DocumentationId(v) for v in self.hasDocumentation]

        if not isinstance(self.requiredByTask, list):
            self.requiredByTask = [self.requiredByTask] if self.requiredByTask is not None else []
        self.requiredByTask = [v if isinstance(v, AiTaskId) else AiTaskId(v) for v in self.requiredByTask]

        if not isinstance(self.implementedByAdapter, list):
            self.implementedByAdapter = [self.implementedByAdapter] if self.implementedByAdapter is not None else []
        self.implementedByAdapter = [v if isinstance(v, AdapterId) else AdapterId(v) for v in self.implementedByAdapter]

        if self.isPartOf is not None and not isinstance(self.isPartOf, CapabilityGroupId):
            self.isPartOf = CapabilityGroupId(self.isPartOf)

        if not isinstance(self.hasJurisdiction, list):
            self.hasJurisdiction = [self.hasJurisdiction] if self.hasJurisdiction is not None else []
        self.hasJurisdiction = [v if isinstance(v, Jurisdiction) else Jurisdiction(v) for v in self.hasJurisdiction]

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class BaseAi(Entity):
    """
    Any type of AI, be it a LLM, RL agent, SVM, etc.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["BaseAi"]
    class_class_curie: ClassVar[str] = "nexus:BaseAi"
    class_name: ClassVar[str] = "BaseAi"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.BaseAi

    id: Union[str, BaseAiId] = None
    producer: Optional[Union[str, OrganizationId]] = None
    hasModelCard: Optional[Union[str, list[str]]] = empty_list()
    hasDocumentation: Optional[Union[Union[str, DocumentationId], list[Union[str, DocumentationId]]]] = empty_list()
    hasLicense: Optional[Union[str, LicenseId]] = None
    performsTask: Optional[Union[Union[str, AiTaskId], list[Union[str, AiTaskId]]]] = empty_list()
    isProvidedBy: Optional[Union[str, AiProviderId]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.producer is not None and not isinstance(self.producer, OrganizationId):
            self.producer = OrganizationId(self.producer)

        if not isinstance(self.hasModelCard, list):
            self.hasModelCard = [self.hasModelCard] if self.hasModelCard is not None else []
        self.hasModelCard = [v if isinstance(v, str) else str(v) for v in self.hasModelCard]

        if not isinstance(self.hasDocumentation, list):
            self.hasDocumentation = [self.hasDocumentation] if self.hasDocumentation is not None else []
        self.hasDocumentation = [v if isinstance(v, DocumentationId) else DocumentationId(v) for v in self.hasDocumentation]

        if self.hasLicense is not None and not isinstance(self.hasLicense, LicenseId):
            self.hasLicense = LicenseId(self.hasLicense)

        if not isinstance(self.performsTask, list):
            self.performsTask = [self.performsTask] if self.performsTask is not None else []
        self.performsTask = [v if isinstance(v, AiTaskId) else AiTaskId(v) for v in self.performsTask]

        if self.isProvidedBy is not None and not isinstance(self.isProvidedBy, AiProviderId):
            self.isProvidedBy = AiProviderId(self.isProvidedBy)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AiSystem(Entry):
    """
    A compound AI System composed of one or more AI capablities. ChatGPT is an example of an AI system which deploys
    multiple GPT AI models.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AIRO["AISystem"]
    class_class_curie: ClassVar[str] = "airo:AISystem"
    class_name: ClassVar[str] = "AiSystem"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.AiSystem

    id: Union[str, AiSystemId] = None
    name: Optional[str] = None
    description: Optional[str] = None
    url: Optional[Union[str, URI]] = None
    dateCreated: Optional[Union[str, XSDDate]] = None
    dateModified: Optional[Union[str, XSDDate]] = None
    exact_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    close_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    related_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    broad_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    isCategorizedAs: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    hasDocumentation: Optional[Union[Union[str, DocumentationId], list[Union[str, DocumentationId]]]] = empty_list()
    isComposedOf: Optional[Union[Union[str, BaseAiId], list[Union[str, BaseAiId]]]] = empty_list()
    hasEuAiSystemType: Optional[Union[str, "AiSystemType"]] = None
    hasEuRiskCategory: Optional[Union[str, "EuAiRiskCategory"]] = None
    hasCapability: Optional[Union[Union[str, CapabilityId], list[Union[str, CapabilityId]]]] = empty_list()
    isAppliedWithinDomain: Optional[Union[Union[str, DomainId], list[Union[str, DomainId]]]] = empty_list()
    isUsedWithinLocality: Optional[Union[Union[str, LocalityOfUseId], list[Union[str, LocalityOfUseId]]]] = empty_list()
    hasPurpose: Optional[Union[Union[str, PurposeId], list[Union[str, PurposeId]]]] = empty_list()
    hasStakeholder: Optional[Union[Union[str, StakeholderId], list[Union[str, StakeholderId]]]] = empty_list()
    isDeployedBy: Optional[Union[str, AIDeployerId]] = None
    isDevelopedBy: Optional[Union[str, AIDeveloperId]] = None
    hasAISubject: Optional[Union[Union[str, AISubjectId], list[Union[str, AISubjectId]]]] = empty_list()
    hasAIUser: Optional[Union[Union[str, AIUserId], list[Union[str, AIUserId]]]] = empty_list()
    hasRelatedRisk: Optional[Union[Union[str, RiskId], list[Union[str, RiskId]]]] = empty_list()
    producer: Optional[Union[str, OrganizationId]] = None
    hasModelCard: Optional[Union[str, list[str]]] = empty_list()
    hasLicense: Optional[Union[str, LicenseId]] = None
    performsTask: Optional[Union[Union[str, AiTaskId], list[Union[str, AiTaskId]]]] = empty_list()
    isProvidedBy: Optional[Union[str, AiProviderId]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AiSystemId):
            self.id = AiSystemId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.url is not None and not isinstance(self.url, URI):
            self.url = URI(self.url)

        if self.dateCreated is not None and not isinstance(self.dateCreated, XSDDate):
            self.dateCreated = XSDDate(self.dateCreated)

        if self.dateModified is not None and not isinstance(self.dateModified, XSDDate):
            self.dateModified = XSDDate(self.dateModified)

        if not isinstance(self.hasDocumentation, list):
            self.hasDocumentation = [self.hasDocumentation] if self.hasDocumentation is not None else []
        self.hasDocumentation = [v if isinstance(v, DocumentationId) else DocumentationId(v) for v in self.hasDocumentation]

        if not isinstance(self.isComposedOf, list):
            self.isComposedOf = [self.isComposedOf] if self.isComposedOf is not None else []
        self.isComposedOf = [v if isinstance(v, BaseAiId) else BaseAiId(v) for v in self.isComposedOf]

        if self.hasEuAiSystemType is not None and not isinstance(self.hasEuAiSystemType, AiSystemType):
            self.hasEuAiSystemType = AiSystemType(self.hasEuAiSystemType)

        if self.hasEuRiskCategory is not None and not isinstance(self.hasEuRiskCategory, EuAiRiskCategory):
            self.hasEuRiskCategory = EuAiRiskCategory(self.hasEuRiskCategory)

        if not isinstance(self.hasCapability, list):
            self.hasCapability = [self.hasCapability] if self.hasCapability is not None else []
        self.hasCapability = [v if isinstance(v, CapabilityId) else CapabilityId(v) for v in self.hasCapability]

        if not isinstance(self.isAppliedWithinDomain, list):
            self.isAppliedWithinDomain = [self.isAppliedWithinDomain] if self.isAppliedWithinDomain is not None else []
        self.isAppliedWithinDomain = [v if isinstance(v, DomainId) else DomainId(v) for v in self.isAppliedWithinDomain]

        if not isinstance(self.isUsedWithinLocality, list):
            self.isUsedWithinLocality = [self.isUsedWithinLocality] if self.isUsedWithinLocality is not None else []
        self.isUsedWithinLocality = [v if isinstance(v, LocalityOfUseId) else LocalityOfUseId(v) for v in self.isUsedWithinLocality]

        if not isinstance(self.hasPurpose, list):
            self.hasPurpose = [self.hasPurpose] if self.hasPurpose is not None else []
        self.hasPurpose = [v if isinstance(v, PurposeId) else PurposeId(v) for v in self.hasPurpose]

        if not isinstance(self.hasStakeholder, list):
            self.hasStakeholder = [self.hasStakeholder] if self.hasStakeholder is not None else []
        self.hasStakeholder = [v if isinstance(v, StakeholderId) else StakeholderId(v) for v in self.hasStakeholder]

        if self.isDeployedBy is not None and not isinstance(self.isDeployedBy, AIDeployerId):
            self.isDeployedBy = AIDeployerId(self.isDeployedBy)

        if self.isDevelopedBy is not None and not isinstance(self.isDevelopedBy, AIDeveloperId):
            self.isDevelopedBy = AIDeveloperId(self.isDevelopedBy)

        if not isinstance(self.hasAISubject, list):
            self.hasAISubject = [self.hasAISubject] if self.hasAISubject is not None else []
        self.hasAISubject = [v if isinstance(v, AISubjectId) else AISubjectId(v) for v in self.hasAISubject]

        if not isinstance(self.hasAIUser, list):
            self.hasAIUser = [self.hasAIUser] if self.hasAIUser is not None else []
        self.hasAIUser = [v if isinstance(v, AIUserId) else AIUserId(v) for v in self.hasAIUser]

        if not isinstance(self.hasRelatedRisk, list):
            self.hasRelatedRisk = [self.hasRelatedRisk] if self.hasRelatedRisk is not None else []
        self.hasRelatedRisk = [v if isinstance(v, RiskId) else RiskId(v) for v in self.hasRelatedRisk]

        if self.producer is not None and not isinstance(self.producer, OrganizationId):
            self.producer = OrganizationId(self.producer)

        if not isinstance(self.hasModelCard, list):
            self.hasModelCard = [self.hasModelCard] if self.hasModelCard is not None else []
        self.hasModelCard = [v if isinstance(v, str) else str(v) for v in self.hasModelCard]

        if self.hasLicense is not None and not isinstance(self.hasLicense, LicenseId):
            self.hasLicense = LicenseId(self.hasLicense)

        if not isinstance(self.performsTask, list):
            self.performsTask = [self.performsTask] if self.performsTask is not None else []
        self.performsTask = [v if isinstance(v, AiTaskId) else AiTaskId(v) for v in self.performsTask]

        if self.isProvidedBy is not None and not isinstance(self.isProvidedBy, AiProviderId):
            self.isProvidedBy = AiProviderId(self.isProvidedBy)

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class AiAgent(AiSystem):
    """
    An artificial intelligence (AI) agent refers to a system or program that is capable of autonomously performing
    tasks on behalf of a user or another system by designing its workflow and utilizing available tools.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["AiAgent"]
    class_class_curie: ClassVar[str] = "nexus:AiAgent"
    class_name: ClassVar[str] = "AiAgent"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.AiAgent

    id: Union[str, AiAgentId] = None
    isProvidedBy: Optional[Union[str, AiProviderId]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.isProvidedBy is not None and not isinstance(self.isProvidedBy, AiProviderId):
            self.isProvidedBy = AiProviderId(self.isProvidedBy)

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class AiModel(BaseAi):
    """
    A base AI Model class. No assumption about the type (SVM, LLM, etc.). Subclassed by model types (see
    LargeLanguageModel).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["AiModel"]
    class_class_curie: ClassVar[str] = "nexus:AiModel"
    class_name: ClassVar[str] = "AiModel"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.AiModel

    id: Union[str, AiModelId] = None
    name: Optional[str] = None
    description: Optional[str] = None
    url: Optional[Union[str, URI]] = None
    dateCreated: Optional[Union[str, XSDDate]] = None
    dateModified: Optional[Union[str, XSDDate]] = None
    exact_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    close_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    related_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    broad_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    isCategorizedAs: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    hasEvaluation: Optional[Union[Union[str, AiEvalResultId], list[Union[str, AiEvalResultId]]]] = empty_list()
    architecture: Optional[str] = None
    gpu_hours: Optional[int] = None
    power_consumption_w: Optional[int] = None
    carbon_emitted: Optional[float] = None
    hasRiskControl: Optional[Union[Union[str, RiskControlId], list[Union[str, RiskControlId]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AiModelId):
            self.id = AiModelId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.url is not None and not isinstance(self.url, URI):
            self.url = URI(self.url)

        if self.dateCreated is not None and not isinstance(self.dateCreated, XSDDate):
            self.dateCreated = XSDDate(self.dateCreated)

        if self.dateModified is not None and not isinstance(self.dateModified, XSDDate):
            self.dateModified = XSDDate(self.dateModified)

        if not isinstance(self.hasEvaluation, list):
            self.hasEvaluation = [self.hasEvaluation] if self.hasEvaluation is not None else []
        self.hasEvaluation = [v if isinstance(v, AiEvalResultId) else AiEvalResultId(v) for v in self.hasEvaluation]

        if self.architecture is not None and not isinstance(self.architecture, str):
            self.architecture = str(self.architecture)

        if self.gpu_hours is not None and not isinstance(self.gpu_hours, int):
            self.gpu_hours = int(self.gpu_hours)

        if self.power_consumption_w is not None and not isinstance(self.power_consumption_w, int):
            self.power_consumption_w = int(self.power_consumption_w)

        if self.carbon_emitted is not None and not isinstance(self.carbon_emitted, float):
            self.carbon_emitted = float(self.carbon_emitted)

        if not isinstance(self.hasRiskControl, list):
            self.hasRiskControl = [self.hasRiskControl] if self.hasRiskControl is not None else []
        self.hasRiskControl = [v if isinstance(v, RiskControlId) else RiskControlId(v) for v in self.hasRiskControl]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class LargeLanguageModel(AiModel):
    """
    A large language model (LLM) is an AI model which supports a range of language-related tasks such as generation,
    summarization, classification, among others. A LLM is implemented as an artificial neural networks using a
    transformer architecture.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["LargeLanguageModel"]
    class_class_curie: ClassVar[str] = "nexus:LargeLanguageModel"
    class_name: ClassVar[str] = "LargeLanguageModel"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.LargeLanguageModel

    id: Union[str, LargeLanguageModelId] = None
    numParameters: Optional[int] = None
    numTrainingTokens: Optional[int] = None
    contextWindowSize: Optional[int] = None
    hasInputModality: Optional[Union[Union[str, ModalityId], list[Union[str, ModalityId]]]] = empty_list()
    hasOutputModality: Optional[Union[Union[str, ModalityId], list[Union[str, ModalityId]]]] = empty_list()
    hasTrainingData: Optional[Union[Union[str, DatasetId], list[Union[str, DatasetId]]]] = empty_list()
    fine_tuning: Optional[str] = None
    supported_languages: Optional[Union[str, list[str]]] = empty_list()
    isPartOf: Optional[Union[str, LargeLanguageModelFamilyId]] = None
    requiresCapability: Optional[Union[Union[str, CapabilityId], list[Union[str, CapabilityId]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.numParameters is not None and not isinstance(self.numParameters, int):
            self.numParameters = int(self.numParameters)

        if self.numTrainingTokens is not None and not isinstance(self.numTrainingTokens, int):
            self.numTrainingTokens = int(self.numTrainingTokens)

        if self.contextWindowSize is not None and not isinstance(self.contextWindowSize, int):
            self.contextWindowSize = int(self.contextWindowSize)

        if not isinstance(self.hasInputModality, list):
            self.hasInputModality = [self.hasInputModality] if self.hasInputModality is not None else []
        self.hasInputModality = [v if isinstance(v, ModalityId) else ModalityId(v) for v in self.hasInputModality]

        if not isinstance(self.hasOutputModality, list):
            self.hasOutputModality = [self.hasOutputModality] if self.hasOutputModality is not None else []
        self.hasOutputModality = [v if isinstance(v, ModalityId) else ModalityId(v) for v in self.hasOutputModality]

        if not isinstance(self.hasTrainingData, list):
            self.hasTrainingData = [self.hasTrainingData] if self.hasTrainingData is not None else []
        self.hasTrainingData = [v if isinstance(v, DatasetId) else DatasetId(v) for v in self.hasTrainingData]

        if self.fine_tuning is not None and not isinstance(self.fine_tuning, str):
            self.fine_tuning = str(self.fine_tuning)

        if not isinstance(self.supported_languages, list):
            self.supported_languages = [self.supported_languages] if self.supported_languages is not None else []
        self.supported_languages = [v if isinstance(v, str) else str(v) for v in self.supported_languages]

        if self.isPartOf is not None and not isinstance(self.isPartOf, LargeLanguageModelFamilyId):
            self.isPartOf = LargeLanguageModelFamilyId(self.isPartOf)

        if not isinstance(self.requiresCapability, list):
            self.requiresCapability = [self.requiresCapability] if self.requiresCapability is not None else []
        self.requiresCapability = [v if isinstance(v, CapabilityId) else CapabilityId(v) for v in self.requiresCapability]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class LargeLanguageModelFamily(Entity):
    """
    A large language model family is a set of models that are provided by the same AI systems provider and are built
    around the same architecture, but differ e.g. in the number of parameters. Examples are Meta's Llama2 family or
    the IBM granite models.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["LargeLanguageModelFamily"]
    class_class_curie: ClassVar[str] = "nexus:LargeLanguageModelFamily"
    class_name: ClassVar[str] = "LargeLanguageModelFamily"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.LargeLanguageModelFamily

    id: Union[str, LargeLanguageModelFamilyId] = None
    hasDocumentation: Optional[Union[Union[str, DocumentationId], list[Union[str, DocumentationId]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, LargeLanguageModelFamilyId):
            self.id = LargeLanguageModelFamilyId(self.id)

        if not isinstance(self.hasDocumentation, list):
            self.hasDocumentation = [self.hasDocumentation] if self.hasDocumentation is not None else []
        self.hasDocumentation = [v if isinstance(v, DocumentationId) else DocumentationId(v) for v in self.hasDocumentation]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AiTask(Entry):
    """
    A task, such as summarization and classification, performed by an AI.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AIRO["AiCapability"]
    class_class_curie: ClassVar[str] = "airo:AiCapability"
    class_name: ClassVar[str] = "AiTask"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.AiTask

    id: Union[str, AiTaskId] = None
    requiresCapability: Optional[Union[Union[str, CapabilityId], list[Union[str, CapabilityId]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AiTaskId):
            self.id = AiTaskId(self.id)

        if not isinstance(self.requiresCapability, list):
            self.requiresCapability = [self.requiresCapability] if self.requiresCapability is not None else []
        self.requiresCapability = [v if isinstance(v, CapabilityId) else CapabilityId(v) for v in self.requiresCapability]

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class AiTaskTaxonomy(Taxonomy):
    """
    A taxonomy of AI Tasks
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["AiTaskTaxonomy"]
    class_class_curie: ClassVar[str] = "nexus:AiTaskTaxonomy"
    class_name: ClassVar[str] = "AiTaskTaxonomy"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.AiTaskTaxonomy

    id: Union[str, AiTaskTaxonomyId] = None
    version: Optional[str] = None
    hasDocumentation: Optional[Union[Union[str, DocumentationId], list[Union[str, DocumentationId]]]] = empty_list()
    hasLicense: Optional[Union[str, LicenseId]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AiTaskTaxonomyId):
            self.id = AiTaskTaxonomyId(self.id)

        if self.version is not None and not isinstance(self.version, str):
            self.version = str(self.version)

        if not isinstance(self.hasDocumentation, list):
            self.hasDocumentation = [self.hasDocumentation] if self.hasDocumentation is not None else []
        self.hasDocumentation = [v if isinstance(v, DocumentationId) else DocumentationId(v) for v in self.hasDocumentation]

        if self.hasLicense is not None and not isinstance(self.hasLicense, LicenseId):
            self.hasLicense = LicenseId(self.hasLicense)

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class AiTaskDomain(Group):
    """
    A grouping of AI Tasks by domain.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["AiTaskDomain"]
    class_class_curie: ClassVar[str] = "nexus:AiTaskDomain"
    class_name: ClassVar[str] = "AiTaskDomain"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.AiTaskDomain

    id: Union[str, AiTaskDomainId] = None
    isDefinedByTaxonomy: Optional[Union[str, TaxonomyId]] = None
    hasPart: Optional[Union[Union[str, AiTaskGroupId], list[Union[str, AiTaskGroupId]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AiTaskDomainId):
            self.id = AiTaskDomainId(self.id)

        if self.isDefinedByTaxonomy is not None and not isinstance(self.isDefinedByTaxonomy, TaxonomyId):
            self.isDefinedByTaxonomy = TaxonomyId(self.isDefinedByTaxonomy)

        if not isinstance(self.hasPart, list):
            self.hasPart = [self.hasPart] if self.hasPart is not None else []
        self.hasPart = [v if isinstance(v, AiTaskGroupId) else AiTaskGroupId(v) for v in self.hasPart]

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class AiTaskGroup(Group):
    """
    A group of AI Tasks.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["AiTaskGroup"]
    class_class_curie: ClassVar[str] = "nexus:AiTaskGroup"
    class_name: ClassVar[str] = "AiTaskGroup"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.AiTaskGroup

    id: Union[str, AiTaskGroupId] = None
    isDefinedByTaxonomy: Optional[Union[str, TaxonomyId]] = None
    hasPart: Optional[Union[Union[str, AiTaskId], list[Union[str, AiTaskId]]]] = empty_list()
    isPartOf: Optional[Union[str, AiTaskDomainId]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AiTaskGroupId):
            self.id = AiTaskGroupId(self.id)

        if self.isDefinedByTaxonomy is not None and not isinstance(self.isDefinedByTaxonomy, TaxonomyId):
            self.isDefinedByTaxonomy = TaxonomyId(self.isDefinedByTaxonomy)

        if not isinstance(self.hasPart, list):
            self.hasPart = [self.hasPart] if self.hasPart is not None else []
        self.hasPart = [v if isinstance(v, AiTaskId) else AiTaskId(v) for v in self.hasPart]

        if self.isPartOf is not None and not isinstance(self.isPartOf, AiTaskDomainId):
            self.isPartOf = AiTaskDomainId(self.isPartOf)

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class AiLifecyclePhase(Entity):
    """
    A Phase of AI lifecycle which indicates evolution of the system from conception through retirement.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AIRO["AILifecyclePhase"]
    class_class_curie: ClassVar[str] = "airo:AILifecyclePhase"
    class_name: ClassVar[str] = "AiLifecyclePhase"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.AiLifecyclePhase

    id: Union[str, AiLifecyclePhaseId] = None

@dataclass(repr=False)
class DataPreprocessing(AiLifecyclePhase):
    """
    Data transformations, such as PI filtering, performed to ensure high quality of AI model training data.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["DataPreprocessing"]
    class_class_curie: ClassVar[str] = "nexus:DataPreprocessing"
    class_name: ClassVar[str] = "DataPreprocessing"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.DataPreprocessing

    id: Union[str, DataPreprocessingId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DataPreprocessingId):
            self.id = DataPreprocessingId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AiModelValidation(AiLifecyclePhase):
    """
    AI model validation steps that have been performed after the model training to ensure high AI model quality.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["AiModelValidation"]
    class_class_curie: ClassVar[str] = "nexus:AiModelValidation"
    class_name: ClassVar[str] = "AiModelValidation"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.AiModelValidation

    id: Union[str, AiModelValidationId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AiModelValidationId):
            self.id = AiModelValidationId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AiProvider(Organization):
    """
    A provider under the AI Act is defined by Article 3(3) as a natural or legal person or body that develops an AI
    system or general-purpose AI model or has an AI system or general-purpose AI model developed; and places that
    ystem or model on the market, or puts that system into service, under the provider's own name or trademark,
    whether for payment or free for charge.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AIRO["AIProvider"]
    class_class_curie: ClassVar[str] = "airo:AIProvider"
    class_name: ClassVar[str] = "AiProvider"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.AiProvider

    id: Union[str, AiProviderId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AiProviderId):
            self.id = AiProviderId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Modality(Entity):
    """
    A modality supported by an Ai component. Examples include text, image, video.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AIRO["Modality"]
    class_class_curie: ClassVar[str] = "airo:Modality"
    class_name: ClassVar[str] = "Modality"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.Modality

    id: Union[str, ModalityId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ModalityId):
            self.id = ModalityId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Input(Entity):
    """
    Input for which the system or component generates output.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AIRO["Input"]
    class_class_curie: ClassVar[str] = "airo:Input"
    class_name: ClassVar[str] = "Input"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.Input

    id: Union[str, InputId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, InputId):
            self.id = InputId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Purpose(Entry):
    """
    The end goal for which an entity is used or an action is taken.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AIRO["Purpose"]
    class_class_curie: ClassVar[str] = "airo:Purpose"
    class_name: ClassVar[str] = "Purpose"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.Purpose

    id: Union[str, PurposeId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PurposeId):
            self.id = PurposeId(self.id)

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class Domain(Entry):
    """
    An area, sector, or industry that is associated with economic activities.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AIRO["Domain"]
    class_class_curie: ClassVar[str] = "airo:Domain"
    class_name: ClassVar[str] = "Domain"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.Domain

    id: Union[str, DomainId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DomainId):
            self.id = DomainId(self.id)

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class LocalityOfUse(Entry):
    """
    The area, e.g. facility or institution, in which an entity is used.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AIRO["LocalityOfUse"]
    class_class_curie: ClassVar[str] = "airo:LocalityOfUse"
    class_name: ClassVar[str] = "LocalityOfUse"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.LocalityOfUse

    id: Union[str, LocalityOfUseId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, LocalityOfUseId):
            self.id = LocalityOfUseId(self.id)

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class AIComponent(Entity):
    """
    Component (element) of an AI system
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AIRO["AIComponent"]
    class_class_curie: ClassVar[str] = "airo:AIComponent"
    class_name: ClassVar[str] = "AIComponent"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.AIComponent

    id: Union[str, AIComponentId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AIComponentId):
            self.id = AIComponentId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Stakeholder(Entity):
    """
    Represents any individual, group or organization that can affect, be affected by or perceive itself to be affected
    by a decision or activity.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AIRO["Stakeholder"]
    class_class_curie: ClassVar[str] = "airo:Stakeholder"
    class_name: ClassVar[str] = "Stakeholder"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.Stakeholder

    id: Union[str, StakeholderId] = None
    isDefinedByTaxonomy: Optional[Union[str, TaxonomyId]] = None
    isPartOf: Optional[Union[str, StakeholderGroupId]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, StakeholderId):
            self.id = StakeholderId(self.id)

        if self.isDefinedByTaxonomy is not None and not isinstance(self.isDefinedByTaxonomy, TaxonomyId):
            self.isDefinedByTaxonomy = TaxonomyId(self.isDefinedByTaxonomy)

        if self.isPartOf is not None and not isinstance(self.isPartOf, StakeholderGroupId):
            self.isPartOf = StakeholderGroupId(self.isPartOf)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AISubject(Stakeholder):
    """
    An entity that is subject to or impacted by the use of AI.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AIRO["AISubject"]
    class_class_curie: ClassVar[str] = "airo:AISubject"
    class_name: ClassVar[str] = "AISubject"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.AISubject

    id: Union[str, AISubjectId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AISubjectId):
            self.id = AISubjectId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AIOperator(Stakeholder):
    """
    Refers to a provider, product manufacturer, deployer, authorised representative, importer or distributor.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AIRO["AIOperator"]
    class_class_curie: ClassVar[str] = "airo:AIOperator"
    class_name: ClassVar[str] = "AIOperator"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.AIOperator

    id: Union[str, AIOperatorId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AIOperatorId):
            self.id = AIOperatorId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AIDeveloper(Stakeholder):
    """
    An organisation or entity that is concerned with the development of AI services and products.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AIRO["AIDeveloper"]
    class_class_curie: ClassVar[str] = "airo:AIDeveloper"
    class_name: ClassVar[str] = "AIDeveloper"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.AIDeveloper

    id: Union[str, AIDeveloperId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AIDeveloperId):
            self.id = AIDeveloperId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AIDeployer(AIOperator):
    """
    Any natural or legal person, public authority, agency or other body using an AI system under its authority except
    where the AI system is used in the course of a personal non-professional activity.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AIRO["AIDeployer"]
    class_class_curie: ClassVar[str] = "airo:AIDeployer"
    class_name: ClassVar[str] = "AIDeployer"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.AIDeployer

    id: Union[str, AIDeployerId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AIDeployerId):
            self.id = AIDeployerId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AIUser(Stakeholder):
    """
    Individual or group that interacts with a system.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AIRO["AIUser"]
    class_class_curie: ClassVar[str] = "airo:AIUser"
    class_name: ClassVar[str] = "AIUser"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.AIUser

    id: Union[str, AIUserId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AIUserId):
            self.id = AIUserId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class StakeholderGroup(Group):
    """
    An AI system stakeholder grouping.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["StakeholderGroup"]
    class_class_curie: ClassVar[str] = "nexus:StakeholderGroup"
    class_name: ClassVar[str] = "StakeholderGroup"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.StakeholderGroup

    id: Union[str, StakeholderGroupId] = None
    isDefinedByTaxonomy: Optional[Union[str, TaxonomyId]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, StakeholderGroupId):
            self.id = StakeholderGroupId(self.id)

        if self.isDefinedByTaxonomy is not None and not isinstance(self.isDefinedByTaxonomy, TaxonomyId):
            self.isDefinedByTaxonomy = TaxonomyId(self.isDefinedByTaxonomy)

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class AiEval(Entity):
    """
    An AI Evaluation, e.g. a metric, benchmark, unitxt card evaluation, a question or a combination of such entities.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DQV["Metric"]
    class_class_curie: ClassVar[str] = "dqv:Metric"
    class_name: ClassVar[str] = "AiEval"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.AiEval

    id: Union[str, AiEvalId] = None
    hasDocumentation: Optional[Union[Union[str, DocumentationId], list[Union[str, DocumentationId]]]] = empty_list()
    hasDataset: Optional[Union[Union[str, DatasetId], list[Union[str, DatasetId]]]] = empty_list()
    hasTasks: Optional[Union[str, list[str]]] = empty_list()
    hasImplementation: Optional[Union[Union[str, URI], list[Union[str, URI]]]] = empty_list()
    hasUnitxtCard: Optional[Union[Union[str, URI], list[Union[str, URI]]]] = empty_list()
    hasLicense: Optional[Union[str, LicenseId]] = None
    hasRelatedRisk: Optional[Union[Union[str, RiskId], list[Union[str, RiskId]]]] = empty_list()
    bestValue: Optional[str] = None
    hasBenchmarkMetadata: Optional[Union[Union[str, BenchmarkMetadataCardId], list[Union[str, BenchmarkMetadataCardId]]]] = empty_list()
    isComposedOf: Optional[Union[Union[str, AiEvalId], list[Union[str, AiEvalId]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AiEvalId):
            self.id = AiEvalId(self.id)

        if not isinstance(self.hasDocumentation, list):
            self.hasDocumentation = [self.hasDocumentation] if self.hasDocumentation is not None else []
        self.hasDocumentation = [v if isinstance(v, DocumentationId) else DocumentationId(v) for v in self.hasDocumentation]

        if not isinstance(self.hasDataset, list):
            self.hasDataset = [self.hasDataset] if self.hasDataset is not None else []
        self.hasDataset = [v if isinstance(v, DatasetId) else DatasetId(v) for v in self.hasDataset]

        if not isinstance(self.hasTasks, list):
            self.hasTasks = [self.hasTasks] if self.hasTasks is not None else []
        self.hasTasks = [v if isinstance(v, str) else str(v) for v in self.hasTasks]

        if not isinstance(self.hasImplementation, list):
            self.hasImplementation = [self.hasImplementation] if self.hasImplementation is not None else []
        self.hasImplementation = [v if isinstance(v, URI) else URI(v) for v in self.hasImplementation]

        if not isinstance(self.hasUnitxtCard, list):
            self.hasUnitxtCard = [self.hasUnitxtCard] if self.hasUnitxtCard is not None else []
        self.hasUnitxtCard = [v if isinstance(v, URI) else URI(v) for v in self.hasUnitxtCard]

        if self.hasLicense is not None and not isinstance(self.hasLicense, LicenseId):
            self.hasLicense = LicenseId(self.hasLicense)

        if not isinstance(self.hasRelatedRisk, list):
            self.hasRelatedRisk = [self.hasRelatedRisk] if self.hasRelatedRisk is not None else []
        self.hasRelatedRisk = [v if isinstance(v, RiskId) else RiskId(v) for v in self.hasRelatedRisk]

        if self.bestValue is not None and not isinstance(self.bestValue, str):
            self.bestValue = str(self.bestValue)

        if not isinstance(self.hasBenchmarkMetadata, list):
            self.hasBenchmarkMetadata = [self.hasBenchmarkMetadata] if self.hasBenchmarkMetadata is not None else []
        self.hasBenchmarkMetadata = [v if isinstance(v, BenchmarkMetadataCardId) else BenchmarkMetadataCardId(v) for v in self.hasBenchmarkMetadata]

        if not isinstance(self.isComposedOf, list):
            self.isComposedOf = [self.isComposedOf] if self.isComposedOf is not None else []
        self.isComposedOf = [v if isinstance(v, AiEvalId) else AiEvalId(v) for v in self.isComposedOf]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AiEvalResult(Entity):
    """
    The result of an evaluation for a specific AI model.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DQV["QualityMeasurement"]
    class_class_curie: ClassVar[str] = "dqv:QualityMeasurement"
    class_name: ClassVar[str] = "AiEvalResult"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.AiEvalResult

    id: Union[str, AiEvalResultId] = None
    value: str = None
    isResultOf: Optional[Union[str, AiEvalId]] = None
    evidence: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AiEvalResultId):
            self.id = AiEvalResultId(self.id)

        if self._is_empty(self.value):
            self.MissingRequiredField("value")
        if not isinstance(self.value, str):
            self.value = str(self.value)

        if self.isResultOf is not None and not isinstance(self.isResultOf, AiEvalId):
            self.isResultOf = AiEvalId(self.isResultOf)

        if self.evidence is not None and not isinstance(self.evidence, str):
            self.evidence = str(self.evidence)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SourceMetadata(Entity):
    """
    Metadata about the source of an evaluation
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["sourcemetadata"]
    class_class_curie: ClassVar[str] = "nexus:sourcemetadata"
    class_name: ClassVar[str] = "SourceMetadata"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.SourceMetadata

    id: Union[str, SourceMetadataId] = None
    source_name: Optional[str] = None
    source_type: Optional[str] = None
    source_organization_name: Optional[str] = None
    source_organization_url: Optional[Union[str, URI]] = None
    evaluator_relationship: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, SourceMetadataId):
            self.id = SourceMetadataId(self.id)

        if self.source_name is not None and not isinstance(self.source_name, str):
            self.source_name = str(self.source_name)

        if self.source_type is not None and not isinstance(self.source_type, str):
            self.source_type = str(self.source_type)

        if self.source_organization_name is not None and not isinstance(self.source_organization_name, str):
            self.source_organization_name = str(self.source_organization_name)

        if self.source_organization_url is not None and not isinstance(self.source_organization_url, URI):
            self.source_organization_url = URI(self.source_organization_url)

        if self.evaluator_relationship is not None and not isinstance(self.evaluator_relationship, str):
            self.evaluator_relationship = str(self.evaluator_relationship)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ModelInfo(Entity):
    """
    Information about the AI model being evaluated
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["modelinfo"]
    class_class_curie: ClassVar[str] = "nexus:modelinfo"
    class_name: ClassVar[str] = "ModelInfo"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.ModelInfo

    id: Union[str, ModelInfoId] = None
    model_name: Optional[str] = None
    model_id: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ModelInfoId):
            self.id = ModelInfoId(self.id)

        if self.model_name is not None and not isinstance(self.model_name, str):
            self.model_name = str(self.model_name)

        if self.model_id is not None and not isinstance(self.model_id, str):
            self.model_id = str(self.model_id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SourceData(Entity):
    """
    Information about the data source used in evaluation
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["sourcedata"]
    class_class_curie: ClassVar[str] = "nexus:sourcedata"
    class_name: ClassVar[str] = "SourceData"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.SourceData

    id: Union[str, SourceDataId] = None
    dataset_name: Optional[str] = None
    source_type: Optional[str] = None
    hf_repo: Optional[str] = None
    hf_split: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, SourceDataId):
            self.id = SourceDataId(self.id)

        if self.dataset_name is not None and not isinstance(self.dataset_name, str):
            self.dataset_name = str(self.dataset_name)

        if self.source_type is not None and not isinstance(self.source_type, str):
            self.source_type = str(self.source_type)

        if self.hf_repo is not None and not isinstance(self.hf_repo, str):
            self.hf_repo = str(self.hf_repo)

        if self.hf_split is not None and not isinstance(self.hf_split, str):
            self.hf_split = str(self.hf_split)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class MetricConfig(Entity):
    """
    Configuration for evaluation metrics
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["metricconfig"]
    class_class_curie: ClassVar[str] = "nexus:metricconfig"
    class_name: ClassVar[str] = "MetricConfig"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.MetricConfig

    id: Union[str, MetricConfigId] = None
    lower_is_better: Optional[Union[bool, Bool]] = None
    score_type: Optional[str] = None
    min_score: Optional[float] = None
    max_score: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, MetricConfigId):
            self.id = MetricConfigId(self.id)

        if self.lower_is_better is not None and not isinstance(self.lower_is_better, Bool):
            self.lower_is_better = Bool(self.lower_is_better)

        if self.score_type is not None and not isinstance(self.score_type, str):
            self.score_type = str(self.score_type)

        if self.min_score is not None and not isinstance(self.min_score, float):
            self.min_score = float(self.min_score)

        if self.max_score is not None and not isinstance(self.max_score, float):
            self.max_score = float(self.max_score)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ScoreDetails(Entity):
    """
    Details about evaluation scores
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["scoredetails"]
    class_class_curie: ClassVar[str] = "nexus:scoredetails"
    class_name: ClassVar[str] = "ScoreDetails"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.ScoreDetails

    id: Union[str, ScoreDetailsId] = None
    score: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ScoreDetailsId):
            self.id = ScoreDetailsId(self.id)

        if self.score is not None and not isinstance(self.score, float):
            self.score = float(self.score)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class EvaluationResultRecord(Entity):
    """
    A single evaluation result record
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["evaluationresultrecord"]
    class_class_curie: ClassVar[str] = "nexus:evaluationresultrecord"
    class_name: ClassVar[str] = "EvaluationResultRecord"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.EvaluationResultRecord

    id: Union[str, EvaluationResultRecordId] = None
    hasSourceData: Optional[Union[dict, SourceData]] = None
    hasMetricConfig: Optional[Union[dict, MetricConfig]] = None
    hasScoreDetails: Optional[Union[dict, ScoreDetails]] = None
    evaluation_name: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, EvaluationResultRecordId):
            self.id = EvaluationResultRecordId(self.id)

        if self.hasSourceData is not None and not isinstance(self.hasSourceData, SourceData):
            self.hasSourceData = SourceData(**as_dict(self.hasSourceData))

        if self.hasMetricConfig is not None and not isinstance(self.hasMetricConfig, MetricConfig):
            self.hasMetricConfig = MetricConfig(**as_dict(self.hasMetricConfig))

        if self.hasScoreDetails is not None and not isinstance(self.hasScoreDetails, ScoreDetails):
            self.hasScoreDetails = ScoreDetails(**as_dict(self.hasScoreDetails))

        if self.evaluation_name is not None and not isinstance(self.evaluation_name, str):
            self.evaluation_name = str(self.evaluation_name)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class EveryEvalAIResult(AiEvalResult):
    """
    An evaluation result from the Every Eval Ever dataset, capturing evaluation metadata and results from the
    EEE_datastore.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["everyevalairesult"]
    class_class_curie: ClassVar[str] = "nexus:everyevalairesult"
    class_name: ClassVar[str] = "EveryEvalAIResult"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.EveryEvalAIResult

    id: Union[str, EveryEvalAIResultId] = None
    value: str = None
    hasSourceMetadata: Optional[Union[dict, SourceMetadata]] = None
    hasModelInfo: Optional[Union[dict, ModelInfo]] = None
    hasEvaluationResults: Optional[Union[dict[Union[str, EvaluationResultRecordId], Union[dict, EvaluationResultRecord]], list[Union[dict, EvaluationResultRecord]]]] = empty_dict()
    hasDataType: Optional[Union[str, list[str]]] = empty_list()
    hasDomains: Optional[Union[str, list[str]]] = empty_list()
    hasLanguages: Optional[Union[str, list[str]]] = empty_list()
    hasTasks: Optional[Union[str, list[str]]] = empty_list()
    hasDataSource: Optional[Union[str, list[str]]] = empty_list()
    hasDataSize: Optional[str] = None
    hasDataFormat: Optional[Union[str, list[str]]] = empty_list()
    hasMethods: Optional[Union[str, list[str]]] = empty_list()
    hasMetrics: Optional[Union[str, list[str]]] = empty_list()
    hasLimitations: Optional[Union[str, list[str]]] = empty_list()
    hasGoal: Optional[str] = None
    hasAudience: Optional[Union[str, list[str]]] = empty_list()
    hasResources: Optional[Union[str, list[str]]] = empty_list()
    hasDocumentation: Optional[Union[Union[str, DocumentationId], list[Union[str, DocumentationId]]]] = empty_list()
    hasRelatedRisk: Optional[Union[Union[str, RiskId], list[Union[str, RiskId]]]] = empty_list()
    schema_version: Optional[str] = None
    evaluation_id: Optional[str] = None
    evaluation_timestamp: Optional[Union[str, XSDDateTime]] = None
    retrieved_timestamp: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, EveryEvalAIResultId):
            self.id = EveryEvalAIResultId(self.id)

        if self.hasSourceMetadata is not None and not isinstance(self.hasSourceMetadata, SourceMetadata):
            self.hasSourceMetadata = SourceMetadata(**as_dict(self.hasSourceMetadata))

        if self.hasModelInfo is not None and not isinstance(self.hasModelInfo, ModelInfo):
            self.hasModelInfo = ModelInfo(**as_dict(self.hasModelInfo))

        self._normalize_inlined_as_dict(slot_name="hasEvaluationResults", slot_type=EvaluationResultRecord, key_name="id", keyed=True)

        if not isinstance(self.hasDataType, list):
            self.hasDataType = [self.hasDataType] if self.hasDataType is not None else []
        self.hasDataType = [v if isinstance(v, str) else str(v) for v in self.hasDataType]

        if not isinstance(self.hasDomains, list):
            self.hasDomains = [self.hasDomains] if self.hasDomains is not None else []
        self.hasDomains = [v if isinstance(v, str) else str(v) for v in self.hasDomains]

        if not isinstance(self.hasLanguages, list):
            self.hasLanguages = [self.hasLanguages] if self.hasLanguages is not None else []
        self.hasLanguages = [v if isinstance(v, str) else str(v) for v in self.hasLanguages]

        if not isinstance(self.hasTasks, list):
            self.hasTasks = [self.hasTasks] if self.hasTasks is not None else []
        self.hasTasks = [v if isinstance(v, str) else str(v) for v in self.hasTasks]

        if not isinstance(self.hasDataSource, list):
            self.hasDataSource = [self.hasDataSource] if self.hasDataSource is not None else []
        self.hasDataSource = [v if isinstance(v, str) else str(v) for v in self.hasDataSource]

        if self.hasDataSize is not None and not isinstance(self.hasDataSize, str):
            self.hasDataSize = str(self.hasDataSize)

        if not isinstance(self.hasDataFormat, list):
            self.hasDataFormat = [self.hasDataFormat] if self.hasDataFormat is not None else []
        self.hasDataFormat = [v if isinstance(v, str) else str(v) for v in self.hasDataFormat]

        if not isinstance(self.hasMethods, list):
            self.hasMethods = [self.hasMethods] if self.hasMethods is not None else []
        self.hasMethods = [v if isinstance(v, str) else str(v) for v in self.hasMethods]

        if not isinstance(self.hasMetrics, list):
            self.hasMetrics = [self.hasMetrics] if self.hasMetrics is not None else []
        self.hasMetrics = [v if isinstance(v, str) else str(v) for v in self.hasMetrics]

        if not isinstance(self.hasLimitations, list):
            self.hasLimitations = [self.hasLimitations] if self.hasLimitations is not None else []
        self.hasLimitations = [v if isinstance(v, str) else str(v) for v in self.hasLimitations]

        if self.hasGoal is not None and not isinstance(self.hasGoal, str):
            self.hasGoal = str(self.hasGoal)

        if not isinstance(self.hasAudience, list):
            self.hasAudience = [self.hasAudience] if self.hasAudience is not None else []
        self.hasAudience = [v if isinstance(v, str) else str(v) for v in self.hasAudience]

        if not isinstance(self.hasResources, list):
            self.hasResources = [self.hasResources] if self.hasResources is not None else []
        self.hasResources = [v if isinstance(v, str) else str(v) for v in self.hasResources]

        if not isinstance(self.hasDocumentation, list):
            self.hasDocumentation = [self.hasDocumentation] if self.hasDocumentation is not None else []
        self.hasDocumentation = [v if isinstance(v, DocumentationId) else DocumentationId(v) for v in self.hasDocumentation]

        if not isinstance(self.hasRelatedRisk, list):
            self.hasRelatedRisk = [self.hasRelatedRisk] if self.hasRelatedRisk is not None else []
        self.hasRelatedRisk = [v if isinstance(v, RiskId) else RiskId(v) for v in self.hasRelatedRisk]

        if self.schema_version is not None and not isinstance(self.schema_version, str):
            self.schema_version = str(self.schema_version)

        if self.evaluation_id is not None and not isinstance(self.evaluation_id, str):
            self.evaluation_id = str(self.evaluation_id)

        if self.evaluation_timestamp is not None and not isinstance(self.evaluation_timestamp, XSDDateTime):
            self.evaluation_timestamp = XSDDateTime(self.evaluation_timestamp)

        if self.retrieved_timestamp is not None and not isinstance(self.retrieved_timestamp, str):
            self.retrieved_timestamp = str(self.retrieved_timestamp)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class BenchmarkMetadataCard(Entity):
    """
    Benchmark metadata cards offer a standardized way to document LLM benchmarks clearly and transparently. Inspired
    by Model Cards and Datasheets, Benchmark metadata cards help researchers and practitioners understand exactly what
    benchmarks test, how they relate to real-world risks, and how to interpret their results responsibly. This is an
    implementation of the design set out in BenchmarkCards: Large Language Model and Risk Reporting
    (https://doi.org/10.48550/arXiv.2410.12974)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["benchmarkmetadatacard"]
    class_class_curie: ClassVar[str] = "nexus:benchmarkmetadatacard"
    class_name: ClassVar[str] = "BenchmarkMetadataCard"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.BenchmarkMetadataCard

    id: Union[str, BenchmarkMetadataCardId] = None
    describesAiEval: Optional[Union[Union[str, AiEvalId], list[Union[str, AiEvalId]]]] = empty_list()
    hasDataType: Optional[Union[str, list[str]]] = empty_list()
    hasDomains: Optional[Union[str, list[str]]] = empty_list()
    hasLanguages: Optional[Union[str, list[str]]] = empty_list()
    hasSimilarBenchmarks: Optional[Union[str, list[str]]] = empty_list()
    hasResources: Optional[Union[str, list[str]]] = empty_list()
    hasGoal: Optional[str] = None
    hasAudience: Optional[Union[str, list[str]]] = empty_list()
    hasTasks: Optional[Union[str, list[str]]] = empty_list()
    hasLimitations: Optional[Union[str, list[str]]] = empty_list()
    hasOutOfScopeUses: Optional[Union[str, list[str]]] = empty_list()
    hasDataSource: Optional[Union[str, list[str]]] = empty_list()
    hasDataSize: Optional[str] = None
    hasDataFormat: Optional[Union[str, list[str]]] = empty_list()
    hasAnnotation: Optional[Union[str, list[str]]] = empty_list()
    hasMethods: Optional[Union[str, list[str]]] = empty_list()
    hasMetrics: Optional[Union[str, list[str]]] = empty_list()
    hasCalculation: Optional[Union[str, list[str]]] = empty_list()
    hasInterpretation: Optional[Union[str, list[str]]] = empty_list()
    hasBaselineResults: Optional[Union[str, list[str]]] = empty_list()
    hasValidation: Optional[Union[str, list[str]]] = empty_list()
    hasRelatedRisk: Optional[Union[Union[str, RiskId], list[Union[str, RiskId]]]] = empty_list()
    hasDemographicAnalysis: Optional[Union[str, list[str]]] = empty_list()
    hasConsiderationPrivacyAndAnonymity: Optional[Union[str, list[str]]] = empty_list()
    hasLicense: Optional[Union[str, LicenseId]] = None
    hasConsiderationConsentProcedures: Optional[Union[str, list[str]]] = empty_list()
    hasConsiderationComplianceWithRegulations: Optional[Union[str, list[str]]] = empty_list()
    hasDocumentation: Optional[Union[Union[str, DocumentationId], list[Union[str, DocumentationId]]]] = empty_list()
    name: Optional[str] = None
    overview: Optional[str] = None
    type: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, BenchmarkMetadataCardId):
            self.id = BenchmarkMetadataCardId(self.id)

        if not isinstance(self.describesAiEval, list):
            self.describesAiEval = [self.describesAiEval] if self.describesAiEval is not None else []
        self.describesAiEval = [v if isinstance(v, AiEvalId) else AiEvalId(v) for v in self.describesAiEval]

        if not isinstance(self.hasDataType, list):
            self.hasDataType = [self.hasDataType] if self.hasDataType is not None else []
        self.hasDataType = [v if isinstance(v, str) else str(v) for v in self.hasDataType]

        if not isinstance(self.hasDomains, list):
            self.hasDomains = [self.hasDomains] if self.hasDomains is not None else []
        self.hasDomains = [v if isinstance(v, str) else str(v) for v in self.hasDomains]

        if not isinstance(self.hasLanguages, list):
            self.hasLanguages = [self.hasLanguages] if self.hasLanguages is not None else []
        self.hasLanguages = [v if isinstance(v, str) else str(v) for v in self.hasLanguages]

        if not isinstance(self.hasSimilarBenchmarks, list):
            self.hasSimilarBenchmarks = [self.hasSimilarBenchmarks] if self.hasSimilarBenchmarks is not None else []
        self.hasSimilarBenchmarks = [v if isinstance(v, str) else str(v) for v in self.hasSimilarBenchmarks]

        if not isinstance(self.hasResources, list):
            self.hasResources = [self.hasResources] if self.hasResources is not None else []
        self.hasResources = [v if isinstance(v, str) else str(v) for v in self.hasResources]

        if self.hasGoal is not None and not isinstance(self.hasGoal, str):
            self.hasGoal = str(self.hasGoal)

        if not isinstance(self.hasAudience, list):
            self.hasAudience = [self.hasAudience] if self.hasAudience is not None else []
        self.hasAudience = [v if isinstance(v, str) else str(v) for v in self.hasAudience]

        if not isinstance(self.hasTasks, list):
            self.hasTasks = [self.hasTasks] if self.hasTasks is not None else []
        self.hasTasks = [v if isinstance(v, str) else str(v) for v in self.hasTasks]

        if not isinstance(self.hasLimitations, list):
            self.hasLimitations = [self.hasLimitations] if self.hasLimitations is not None else []
        self.hasLimitations = [v if isinstance(v, str) else str(v) for v in self.hasLimitations]

        if not isinstance(self.hasOutOfScopeUses, list):
            self.hasOutOfScopeUses = [self.hasOutOfScopeUses] if self.hasOutOfScopeUses is not None else []
        self.hasOutOfScopeUses = [v if isinstance(v, str) else str(v) for v in self.hasOutOfScopeUses]

        if not isinstance(self.hasDataSource, list):
            self.hasDataSource = [self.hasDataSource] if self.hasDataSource is not None else []
        self.hasDataSource = [v if isinstance(v, str) else str(v) for v in self.hasDataSource]

        if self.hasDataSize is not None and not isinstance(self.hasDataSize, str):
            self.hasDataSize = str(self.hasDataSize)

        if not isinstance(self.hasDataFormat, list):
            self.hasDataFormat = [self.hasDataFormat] if self.hasDataFormat is not None else []
        self.hasDataFormat = [v if isinstance(v, str) else str(v) for v in self.hasDataFormat]

        if not isinstance(self.hasAnnotation, list):
            self.hasAnnotation = [self.hasAnnotation] if self.hasAnnotation is not None else []
        self.hasAnnotation = [v if isinstance(v, str) else str(v) for v in self.hasAnnotation]

        if not isinstance(self.hasMethods, list):
            self.hasMethods = [self.hasMethods] if self.hasMethods is not None else []
        self.hasMethods = [v if isinstance(v, str) else str(v) for v in self.hasMethods]

        if not isinstance(self.hasMetrics, list):
            self.hasMetrics = [self.hasMetrics] if self.hasMetrics is not None else []
        self.hasMetrics = [v if isinstance(v, str) else str(v) for v in self.hasMetrics]

        if not isinstance(self.hasCalculation, list):
            self.hasCalculation = [self.hasCalculation] if self.hasCalculation is not None else []
        self.hasCalculation = [v if isinstance(v, str) else str(v) for v in self.hasCalculation]

        if not isinstance(self.hasInterpretation, list):
            self.hasInterpretation = [self.hasInterpretation] if self.hasInterpretation is not None else []
        self.hasInterpretation = [v if isinstance(v, str) else str(v) for v in self.hasInterpretation]

        if not isinstance(self.hasBaselineResults, list):
            self.hasBaselineResults = [self.hasBaselineResults] if self.hasBaselineResults is not None else []
        self.hasBaselineResults = [v if isinstance(v, str) else str(v) for v in self.hasBaselineResults]

        if not isinstance(self.hasValidation, list):
            self.hasValidation = [self.hasValidation] if self.hasValidation is not None else []
        self.hasValidation = [v if isinstance(v, str) else str(v) for v in self.hasValidation]

        if not isinstance(self.hasRelatedRisk, list):
            self.hasRelatedRisk = [self.hasRelatedRisk] if self.hasRelatedRisk is not None else []
        self.hasRelatedRisk = [v if isinstance(v, RiskId) else RiskId(v) for v in self.hasRelatedRisk]

        if not isinstance(self.hasDemographicAnalysis, list):
            self.hasDemographicAnalysis = [self.hasDemographicAnalysis] if self.hasDemographicAnalysis is not None else []
        self.hasDemographicAnalysis = [v if isinstance(v, str) else str(v) for v in self.hasDemographicAnalysis]

        if not isinstance(self.hasConsiderationPrivacyAndAnonymity, list):
            self.hasConsiderationPrivacyAndAnonymity = [self.hasConsiderationPrivacyAndAnonymity] if self.hasConsiderationPrivacyAndAnonymity is not None else []
        self.hasConsiderationPrivacyAndAnonymity = [v if isinstance(v, str) else str(v) for v in self.hasConsiderationPrivacyAndAnonymity]

        if self.hasLicense is not None and not isinstance(self.hasLicense, LicenseId):
            self.hasLicense = LicenseId(self.hasLicense)

        if not isinstance(self.hasConsiderationConsentProcedures, list):
            self.hasConsiderationConsentProcedures = [self.hasConsiderationConsentProcedures] if self.hasConsiderationConsentProcedures is not None else []
        self.hasConsiderationConsentProcedures = [v if isinstance(v, str) else str(v) for v in self.hasConsiderationConsentProcedures]

        if not isinstance(self.hasConsiderationComplianceWithRegulations, list):
            self.hasConsiderationComplianceWithRegulations = [self.hasConsiderationComplianceWithRegulations] if self.hasConsiderationComplianceWithRegulations is not None else []
        self.hasConsiderationComplianceWithRegulations = [v if isinstance(v, str) else str(v) for v in self.hasConsiderationComplianceWithRegulations]

        if not isinstance(self.hasDocumentation, list):
            self.hasDocumentation = [self.hasDocumentation] if self.hasDocumentation is not None else []
        self.hasDocumentation = [v if isinstance(v, DocumentationId) else DocumentationId(v) for v in self.hasDocumentation]

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.overview is not None and not isinstance(self.overview, str):
            self.overview = str(self.overview)

        self.type = str(self.class_name)

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class Question(AiEval):
    """
    An evaluation where a question has to be answered
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["Question"]
    class_class_curie: ClassVar[str] = "nexus:Question"
    class_name: ClassVar[str] = "Question"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.Question

    id: Union[str, QuestionId] = None
    text: str = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, QuestionId):
            self.id = QuestionId(self.id)

        if self._is_empty(self.text):
            self.MissingRequiredField("text")
        if not isinstance(self.text, str):
            self.text = str(self.text)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Questionnaire(AiEval):
    """
    A questionnaire groups questions
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["Questionnaire"]
    class_class_curie: ClassVar[str] = "nexus:Questionnaire"
    class_name: ClassVar[str] = "Questionnaire"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.Questionnaire

    id: Union[str, QuestionnaireId] = None
    composed_of: Optional[Union[str, QuestionId]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, QuestionnaireId):
            self.id = QuestionnaireId(self.id)

        if self.composed_of is not None and not isinstance(self.composed_of, QuestionId):
            self.composed_of = QuestionId(self.composed_of)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Adapter(Entry):
    """
    Adapter-based methods add extra trainable parameters after the attention and fully-connected layers of a frozen
    pretrained model to reduce memory-usage and speed up training. The adapters are typically small but demonstrate
    comparable performance to a fully finetuned model and enable training larger models with fewer resources.
    (https://huggingface.co/docs/peft/en/conceptual_guides/adapter)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["Adapter"]
    class_class_curie: ClassVar[str] = "nexus:Adapter"
    class_name: ClassVar[str] = "Adapter"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.Adapter

    id: Union[str, AdapterId] = None
    name: Optional[str] = None
    description: Optional[str] = None
    url: Optional[Union[str, URI]] = None
    dateCreated: Optional[Union[str, XSDDate]] = None
    dateModified: Optional[Union[str, XSDDate]] = None
    exact_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    close_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    related_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    broad_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    isCategorizedAs: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    isPartOf: Optional[str] = None
    hasAdapterType: Optional[Union[Union[str, "AdapterType"], list[Union[str, "AdapterType"]]]] = empty_list()
    isDefinedByVocabulary: Optional[Union[str, VocabularyId]] = None
    hasDocumentation: Optional[Union[Union[str, DocumentationId], list[Union[str, DocumentationId]]]] = empty_list()
    hasLicense: Optional[Union[str, LicenseId]] = None
    hasRelatedRisk: Optional[Union[Union[str, RiskId], list[Union[str, RiskId]]]] = empty_list()
    adaptsModel: Optional[Union[Union[str, LargeLanguageModelId], list[Union[str, LargeLanguageModelId]]]] = empty_list()
    implementsCapability: Optional[Union[Union[str, CapabilityId], list[Union[str, CapabilityId]]]] = empty_list()
    hasCapability: Optional[Union[Union[str, CapabilityId], list[Union[str, CapabilityId]]]] = empty_list()
    requiresCapability: Optional[Union[Union[str, CapabilityId], list[Union[str, CapabilityId]]]] = empty_list()
    producer: Optional[Union[str, OrganizationId]] = None
    hasModelCard: Optional[Union[str, list[str]]] = empty_list()
    performsTask: Optional[Union[Union[str, AiTaskId], list[Union[str, AiTaskId]]]] = empty_list()
    isProvidedBy: Optional[Union[str, AiProviderId]] = None
    hasEvaluation: Optional[Union[Union[str, AiEvalResultId], list[Union[str, AiEvalResultId]]]] = empty_list()
    architecture: Optional[str] = None
    gpu_hours: Optional[int] = None
    power_consumption_w: Optional[int] = None
    carbon_emitted: Optional[float] = None
    hasRiskControl: Optional[Union[Union[str, RiskControlId], list[Union[str, RiskControlId]]]] = empty_list()
    numParameters: Optional[int] = None
    numTrainingTokens: Optional[int] = None
    contextWindowSize: Optional[int] = None
    hasInputModality: Optional[Union[Union[str, ModalityId], list[Union[str, ModalityId]]]] = empty_list()
    hasOutputModality: Optional[Union[Union[str, ModalityId], list[Union[str, ModalityId]]]] = empty_list()
    hasTrainingData: Optional[Union[Union[str, DatasetId], list[Union[str, DatasetId]]]] = empty_list()
    fine_tuning: Optional[str] = None
    supported_languages: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AdapterId):
            self.id = AdapterId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.url is not None and not isinstance(self.url, URI):
            self.url = URI(self.url)

        if self.dateCreated is not None and not isinstance(self.dateCreated, XSDDate):
            self.dateCreated = XSDDate(self.dateCreated)

        if self.dateModified is not None and not isinstance(self.dateModified, XSDDate):
            self.dateModified = XSDDate(self.dateModified)

        if self.isPartOf is not None and not isinstance(self.isPartOf, str):
            self.isPartOf = str(self.isPartOf)

        if not isinstance(self.hasAdapterType, list):
            self.hasAdapterType = [self.hasAdapterType] if self.hasAdapterType is not None else []
        self.hasAdapterType = [v if isinstance(v, AdapterType) else AdapterType(v) for v in self.hasAdapterType]

        if self.isDefinedByVocabulary is not None and not isinstance(self.isDefinedByVocabulary, VocabularyId):
            self.isDefinedByVocabulary = VocabularyId(self.isDefinedByVocabulary)

        if not isinstance(self.hasDocumentation, list):
            self.hasDocumentation = [self.hasDocumentation] if self.hasDocumentation is not None else []
        self.hasDocumentation = [v if isinstance(v, DocumentationId) else DocumentationId(v) for v in self.hasDocumentation]

        if self.hasLicense is not None and not isinstance(self.hasLicense, LicenseId):
            self.hasLicense = LicenseId(self.hasLicense)

        if not isinstance(self.hasRelatedRisk, list):
            self.hasRelatedRisk = [self.hasRelatedRisk] if self.hasRelatedRisk is not None else []
        self.hasRelatedRisk = [v if isinstance(v, RiskId) else RiskId(v) for v in self.hasRelatedRisk]

        if not isinstance(self.adaptsModel, list):
            self.adaptsModel = [self.adaptsModel] if self.adaptsModel is not None else []
        self.adaptsModel = [v if isinstance(v, LargeLanguageModelId) else LargeLanguageModelId(v) for v in self.adaptsModel]

        if not isinstance(self.implementsCapability, list):
            self.implementsCapability = [self.implementsCapability] if self.implementsCapability is not None else []
        self.implementsCapability = [v if isinstance(v, CapabilityId) else CapabilityId(v) for v in self.implementsCapability]

        if not isinstance(self.hasCapability, list):
            self.hasCapability = [self.hasCapability] if self.hasCapability is not None else []
        self.hasCapability = [v if isinstance(v, CapabilityId) else CapabilityId(v) for v in self.hasCapability]

        if not isinstance(self.requiresCapability, list):
            self.requiresCapability = [self.requiresCapability] if self.requiresCapability is not None else []
        self.requiresCapability = [v if isinstance(v, CapabilityId) else CapabilityId(v) for v in self.requiresCapability]

        if self.producer is not None and not isinstance(self.producer, OrganizationId):
            self.producer = OrganizationId(self.producer)

        if not isinstance(self.hasModelCard, list):
            self.hasModelCard = [self.hasModelCard] if self.hasModelCard is not None else []
        self.hasModelCard = [v if isinstance(v, str) else str(v) for v in self.hasModelCard]

        if not isinstance(self.performsTask, list):
            self.performsTask = [self.performsTask] if self.performsTask is not None else []
        self.performsTask = [v if isinstance(v, AiTaskId) else AiTaskId(v) for v in self.performsTask]

        if self.isProvidedBy is not None and not isinstance(self.isProvidedBy, AiProviderId):
            self.isProvidedBy = AiProviderId(self.isProvidedBy)

        if not isinstance(self.hasEvaluation, list):
            self.hasEvaluation = [self.hasEvaluation] if self.hasEvaluation is not None else []
        self.hasEvaluation = [v if isinstance(v, AiEvalResultId) else AiEvalResultId(v) for v in self.hasEvaluation]

        if self.architecture is not None and not isinstance(self.architecture, str):
            self.architecture = str(self.architecture)

        if self.gpu_hours is not None and not isinstance(self.gpu_hours, int):
            self.gpu_hours = int(self.gpu_hours)

        if self.power_consumption_w is not None and not isinstance(self.power_consumption_w, int):
            self.power_consumption_w = int(self.power_consumption_w)

        if self.carbon_emitted is not None and not isinstance(self.carbon_emitted, float):
            self.carbon_emitted = float(self.carbon_emitted)

        if not isinstance(self.hasRiskControl, list):
            self.hasRiskControl = [self.hasRiskControl] if self.hasRiskControl is not None else []
        self.hasRiskControl = [v if isinstance(v, RiskControlId) else RiskControlId(v) for v in self.hasRiskControl]

        if self.numParameters is not None and not isinstance(self.numParameters, int):
            self.numParameters = int(self.numParameters)

        if self.numTrainingTokens is not None and not isinstance(self.numTrainingTokens, int):
            self.numTrainingTokens = int(self.numTrainingTokens)

        if self.contextWindowSize is not None and not isinstance(self.contextWindowSize, int):
            self.contextWindowSize = int(self.contextWindowSize)

        if not isinstance(self.hasInputModality, list):
            self.hasInputModality = [self.hasInputModality] if self.hasInputModality is not None else []
        self.hasInputModality = [v if isinstance(v, ModalityId) else ModalityId(v) for v in self.hasInputModality]

        if not isinstance(self.hasOutputModality, list):
            self.hasOutputModality = [self.hasOutputModality] if self.hasOutputModality is not None else []
        self.hasOutputModality = [v if isinstance(v, ModalityId) else ModalityId(v) for v in self.hasOutputModality]

        if not isinstance(self.hasTrainingData, list):
            self.hasTrainingData = [self.hasTrainingData] if self.hasTrainingData is not None else []
        self.hasTrainingData = [v if isinstance(v, DatasetId) else DatasetId(v) for v in self.hasTrainingData]

        if self.fine_tuning is not None and not isinstance(self.fine_tuning, str):
            self.fine_tuning = str(self.fine_tuning)

        if not isinstance(self.supported_languages, list):
            self.supported_languages = [self.supported_languages] if self.supported_languages is not None else []
        self.supported_languages = [v if isinstance(v, str) else str(v) for v in self.supported_languages]

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class LLMIntrinsic(Entry):
    """
    A capability that can be invoked through a well-defined API that is reasonably stable and independent of how the
    LLM intrinsic itself is implemented.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = AI["Capability"]
    class_class_curie: ClassVar[str] = "ai:Capability"
    class_name: ClassVar[str] = "LLMIntrinsic"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.LLMIntrinsic

    id: Union[str, LLMIntrinsicId] = None
    hasRelatedRisk: Optional[Union[Union[str, RiskId], list[Union[str, RiskId]]]] = empty_list()
    hasRelatedTerm: Optional[Union[Union[str, TermId], list[Union[str, TermId]]]] = empty_list()
    hasDocumentation: Optional[Union[Union[str, DocumentationId], list[Union[str, DocumentationId]]]] = empty_list()
    isDefinedByVocabulary: Optional[Union[str, VocabularyId]] = None
    hasAdapter: Optional[Union[Union[str, AdapterId], list[Union[str, AdapterId]]]] = empty_list()
    hasCapability: Optional[Union[Union[str, CapabilityId], list[Union[str, CapabilityId]]]] = empty_list()
    implementsCapability: Optional[Union[Union[str, CapabilityId], list[Union[str, CapabilityId]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, LLMIntrinsicId):
            self.id = LLMIntrinsicId(self.id)

        if not isinstance(self.hasRelatedRisk, list):
            self.hasRelatedRisk = [self.hasRelatedRisk] if self.hasRelatedRisk is not None else []
        self.hasRelatedRisk = [v if isinstance(v, RiskId) else RiskId(v) for v in self.hasRelatedRisk]

        if not isinstance(self.hasRelatedTerm, list):
            self.hasRelatedTerm = [self.hasRelatedTerm] if self.hasRelatedTerm is not None else []
        self.hasRelatedTerm = [v if isinstance(v, TermId) else TermId(v) for v in self.hasRelatedTerm]

        if not isinstance(self.hasDocumentation, list):
            self.hasDocumentation = [self.hasDocumentation] if self.hasDocumentation is not None else []
        self.hasDocumentation = [v if isinstance(v, DocumentationId) else DocumentationId(v) for v in self.hasDocumentation]

        if self.isDefinedByVocabulary is not None and not isinstance(self.isDefinedByVocabulary, VocabularyId):
            self.isDefinedByVocabulary = VocabularyId(self.isDefinedByVocabulary)

        if not isinstance(self.hasAdapter, list):
            self.hasAdapter = [self.hasAdapter] if self.hasAdapter is not None else []
        self.hasAdapter = [v if isinstance(v, AdapterId) else AdapterId(v) for v in self.hasAdapter]

        if not isinstance(self.hasCapability, list):
            self.hasCapability = [self.hasCapability] if self.hasCapability is not None else []
        self.hasCapability = [v if isinstance(v, CapabilityId) else CapabilityId(v) for v in self.hasCapability]

        if not isinstance(self.implementsCapability, list):
            self.implementsCapability = [self.implementsCapability] if self.implementsCapability is not None else []
        self.implementsCapability = [v if isinstance(v, CapabilityId) else CapabilityId(v) for v in self.implementsCapability]

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class ControlActivity(Rule):
    """
    An obligation, permission, or prohibition for AI system assurance.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["ControlActivity"]
    class_class_curie: ClassVar[str] = "nexus:ControlActivity"
    class_name: ClassVar[str] = "ControlActivity"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.ControlActivity

    id: Union[str, ControlActivityId] = None
    hasControlApplication: Optional[Union[str, "AIUC1ControlApplicationCategory"]] = None
    hasEvidenceCategory: Optional[Union[Union[str, "AIUC1EvidenceCategory"], list[Union[str, "AIUC1EvidenceCategory"]]]] = empty_list()
    hasTypicalLocation: Optional[Union[str, list[str]]] = empty_list()
    appliesToCapability: Optional[Union[Union[str, AiTaskId], list[Union[str, AiTaskId]]]] = empty_list()
    hasRequirement: Optional[Union[str, RequirementId]] = None
    hasRequirementType: Optional[Union[str, "AIUC1RequirementType"]] = None
    hasTypicalEvidence: Optional[str] = None
    type: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.hasControlApplication is not None and not isinstance(self.hasControlApplication, AIUC1ControlApplicationCategory):
            self.hasControlApplication = AIUC1ControlApplicationCategory(self.hasControlApplication)

        if not isinstance(self.hasEvidenceCategory, list):
            self.hasEvidenceCategory = [self.hasEvidenceCategory] if self.hasEvidenceCategory is not None else []
        self.hasEvidenceCategory = [v if isinstance(v, AIUC1EvidenceCategory) else AIUC1EvidenceCategory(v) for v in self.hasEvidenceCategory]

        if not isinstance(self.hasTypicalLocation, list):
            self.hasTypicalLocation = [self.hasTypicalLocation] if self.hasTypicalLocation is not None else []
        self.hasTypicalLocation = [v if isinstance(v, str) else str(v) for v in self.hasTypicalLocation]

        if not isinstance(self.appliesToCapability, list):
            self.appliesToCapability = [self.appliesToCapability] if self.appliesToCapability is not None else []
        self.appliesToCapability = [v if isinstance(v, AiTaskId) else AiTaskId(v) for v in self.appliesToCapability]

        if self.hasRequirement is not None and not isinstance(self.hasRequirement, RequirementId):
            self.hasRequirement = RequirementId(self.hasRequirement)

        if self.hasRequirementType is not None and not isinstance(self.hasRequirementType, AIUC1RequirementType):
            self.hasRequirementType = AIUC1RequirementType(self.hasRequirementType)

        if self.hasTypicalEvidence is not None and not isinstance(self.hasTypicalEvidence, str):
            self.hasTypicalEvidence = str(self.hasTypicalEvidence)

        self.type = str(self.class_name)

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


    def __new__(cls, *args, **kwargs):

        type_designator = "type"
        if not type_designator in kwargs:
            return super().__new__(cls,*args,**kwargs)
        else:
            type_designator_value = kwargs[type_designator]
            target_cls = cls._class_for("class_name", type_designator_value)


            if target_cls is None:
                raise ValueError(f"Wrong type designator value: class {cls.__name__} "
                                 f"has no subclass with ['class_name']='{kwargs[type_designator]}'")
            return super().__new__(target_cls,*args,**kwargs)



@dataclass(repr=False)
class ControlActivityPermission(Permission):
    """
    A control activity (rule) describing a permission to perform an activity
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["ControlActivityPermission"]
    class_class_curie: ClassVar[str] = "nexus:ControlActivityPermission"
    class_name: ClassVar[str] = "ControlActivityPermission"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.ControlActivityPermission

    id: Union[str, ControlActivityPermissionId] = None
    name: Optional[str] = None
    description: Optional[str] = None
    url: Optional[Union[str, URI]] = None
    dateCreated: Optional[Union[str, XSDDate]] = None
    dateModified: Optional[Union[str, XSDDate]] = None
    exact_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    close_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    related_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    broad_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    isCategorizedAs: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    isDefinedByTaxonomy: Optional[Union[str, TaxonomyId]] = None
    hasRule: Optional[Union[Union[str, RuleId], list[Union[str, RuleId]]]] = empty_list()
    type: Optional[str] = None
    hasControlApplication: Optional[Union[str, "AIUC1ControlApplicationCategory"]] = None
    hasEvidenceCategory: Optional[Union[Union[str, "AIUC1EvidenceCategory"], list[Union[str, "AIUC1EvidenceCategory"]]]] = empty_list()
    hasTypicalLocation: Optional[Union[str, list[str]]] = empty_list()
    appliesToCapability: Optional[Union[Union[str, AiTaskId], list[Union[str, AiTaskId]]]] = empty_list()
    hasRequirement: Optional[Union[str, RequirementId]] = None
    hasRequirementType: Optional[Union[str, "AIUC1RequirementType"]] = None
    hasTypicalEvidence: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ControlActivityPermissionId):
            self.id = ControlActivityPermissionId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.url is not None and not isinstance(self.url, URI):
            self.url = URI(self.url)

        if self.dateCreated is not None and not isinstance(self.dateCreated, XSDDate):
            self.dateCreated = XSDDate(self.dateCreated)

        if self.dateModified is not None and not isinstance(self.dateModified, XSDDate):
            self.dateModified = XSDDate(self.dateModified)

        if self.isDefinedByTaxonomy is not None and not isinstance(self.isDefinedByTaxonomy, TaxonomyId):
            self.isDefinedByTaxonomy = TaxonomyId(self.isDefinedByTaxonomy)

        if not isinstance(self.hasRule, list):
            self.hasRule = [self.hasRule] if self.hasRule is not None else []
        self.hasRule = [v if isinstance(v, RuleId) else RuleId(v) for v in self.hasRule]

        self.type = str(self.class_name)

        if self.hasControlApplication is not None and not isinstance(self.hasControlApplication, AIUC1ControlApplicationCategory):
            self.hasControlApplication = AIUC1ControlApplicationCategory(self.hasControlApplication)

        if not isinstance(self.hasEvidenceCategory, list):
            self.hasEvidenceCategory = [self.hasEvidenceCategory] if self.hasEvidenceCategory is not None else []
        self.hasEvidenceCategory = [v if isinstance(v, AIUC1EvidenceCategory) else AIUC1EvidenceCategory(v) for v in self.hasEvidenceCategory]

        if not isinstance(self.hasTypicalLocation, list):
            self.hasTypicalLocation = [self.hasTypicalLocation] if self.hasTypicalLocation is not None else []
        self.hasTypicalLocation = [v if isinstance(v, str) else str(v) for v in self.hasTypicalLocation]

        if not isinstance(self.appliesToCapability, list):
            self.appliesToCapability = [self.appliesToCapability] if self.appliesToCapability is not None else []
        self.appliesToCapability = [v if isinstance(v, AiTaskId) else AiTaskId(v) for v in self.appliesToCapability]

        if self.hasRequirement is not None and not isinstance(self.hasRequirement, RequirementId):
            self.hasRequirement = RequirementId(self.hasRequirement)

        if self.hasRequirementType is not None and not isinstance(self.hasRequirementType, AIUC1RequirementType):
            self.hasRequirementType = AIUC1RequirementType(self.hasRequirementType)

        if self.hasTypicalEvidence is not None and not isinstance(self.hasTypicalEvidence, str):
            self.hasTypicalEvidence = str(self.hasTypicalEvidence)

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class ControlActivityProhibition(Prohibition):
    """
    A control activity (rule) describing a prohibition to perform an activity
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["ControlActivityProhibition"]
    class_class_curie: ClassVar[str] = "nexus:ControlActivityProhibition"
    class_name: ClassVar[str] = "ControlActivityProhibition"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.ControlActivityProhibition

    id: Union[str, ControlActivityProhibitionId] = None
    name: Optional[str] = None
    description: Optional[str] = None
    url: Optional[Union[str, URI]] = None
    dateCreated: Optional[Union[str, XSDDate]] = None
    dateModified: Optional[Union[str, XSDDate]] = None
    exact_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    close_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    related_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    broad_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    isCategorizedAs: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    isDefinedByTaxonomy: Optional[Union[str, TaxonomyId]] = None
    hasRule: Optional[Union[Union[str, RuleId], list[Union[str, RuleId]]]] = empty_list()
    type: Optional[str] = None
    hasControlApplication: Optional[Union[str, "AIUC1ControlApplicationCategory"]] = None
    hasEvidenceCategory: Optional[Union[Union[str, "AIUC1EvidenceCategory"], list[Union[str, "AIUC1EvidenceCategory"]]]] = empty_list()
    hasTypicalLocation: Optional[Union[str, list[str]]] = empty_list()
    appliesToCapability: Optional[Union[Union[str, AiTaskId], list[Union[str, AiTaskId]]]] = empty_list()
    hasRequirement: Optional[Union[str, RequirementId]] = None
    hasRequirementType: Optional[Union[str, "AIUC1RequirementType"]] = None
    hasTypicalEvidence: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ControlActivityProhibitionId):
            self.id = ControlActivityProhibitionId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.url is not None and not isinstance(self.url, URI):
            self.url = URI(self.url)

        if self.dateCreated is not None and not isinstance(self.dateCreated, XSDDate):
            self.dateCreated = XSDDate(self.dateCreated)

        if self.dateModified is not None and not isinstance(self.dateModified, XSDDate):
            self.dateModified = XSDDate(self.dateModified)

        if self.isDefinedByTaxonomy is not None and not isinstance(self.isDefinedByTaxonomy, TaxonomyId):
            self.isDefinedByTaxonomy = TaxonomyId(self.isDefinedByTaxonomy)

        if not isinstance(self.hasRule, list):
            self.hasRule = [self.hasRule] if self.hasRule is not None else []
        self.hasRule = [v if isinstance(v, RuleId) else RuleId(v) for v in self.hasRule]

        self.type = str(self.class_name)

        if self.hasControlApplication is not None and not isinstance(self.hasControlApplication, AIUC1ControlApplicationCategory):
            self.hasControlApplication = AIUC1ControlApplicationCategory(self.hasControlApplication)

        if not isinstance(self.hasEvidenceCategory, list):
            self.hasEvidenceCategory = [self.hasEvidenceCategory] if self.hasEvidenceCategory is not None else []
        self.hasEvidenceCategory = [v if isinstance(v, AIUC1EvidenceCategory) else AIUC1EvidenceCategory(v) for v in self.hasEvidenceCategory]

        if not isinstance(self.hasTypicalLocation, list):
            self.hasTypicalLocation = [self.hasTypicalLocation] if self.hasTypicalLocation is not None else []
        self.hasTypicalLocation = [v if isinstance(v, str) else str(v) for v in self.hasTypicalLocation]

        if not isinstance(self.appliesToCapability, list):
            self.appliesToCapability = [self.appliesToCapability] if self.appliesToCapability is not None else []
        self.appliesToCapability = [v if isinstance(v, AiTaskId) else AiTaskId(v) for v in self.appliesToCapability]

        if self.hasRequirement is not None and not isinstance(self.hasRequirement, RequirementId):
            self.hasRequirement = RequirementId(self.hasRequirement)

        if self.hasRequirementType is not None and not isinstance(self.hasRequirementType, AIUC1RequirementType):
            self.hasRequirementType = AIUC1RequirementType(self.hasRequirementType)

        if self.hasTypicalEvidence is not None and not isinstance(self.hasTypicalEvidence, str):
            self.hasTypicalEvidence = str(self.hasTypicalEvidence)

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class ControlActivityObligation(Obligation):
    """
    A control activity (rule) describing an obligation for performing an activity
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["ControlActivityObligation"]
    class_class_curie: ClassVar[str] = "nexus:ControlActivityObligation"
    class_name: ClassVar[str] = "ControlActivityObligation"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.ControlActivityObligation

    id: Union[str, ControlActivityObligationId] = None
    name: Optional[str] = None
    description: Optional[str] = None
    url: Optional[Union[str, URI]] = None
    dateCreated: Optional[Union[str, XSDDate]] = None
    dateModified: Optional[Union[str, XSDDate]] = None
    exact_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    close_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    related_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    broad_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    isCategorizedAs: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    isDefinedByTaxonomy: Optional[Union[str, TaxonomyId]] = None
    hasRule: Optional[Union[Union[str, RuleId], list[Union[str, RuleId]]]] = empty_list()
    type: Optional[str] = None
    hasControlApplication: Optional[Union[str, "AIUC1ControlApplicationCategory"]] = None
    hasEvidenceCategory: Optional[Union[Union[str, "AIUC1EvidenceCategory"], list[Union[str, "AIUC1EvidenceCategory"]]]] = empty_list()
    hasTypicalLocation: Optional[Union[str, list[str]]] = empty_list()
    appliesToCapability: Optional[Union[Union[str, AiTaskId], list[Union[str, AiTaskId]]]] = empty_list()
    hasRequirement: Optional[Union[str, RequirementId]] = None
    hasRequirementType: Optional[Union[str, "AIUC1RequirementType"]] = None
    hasTypicalEvidence: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ControlActivityObligationId):
            self.id = ControlActivityObligationId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.url is not None and not isinstance(self.url, URI):
            self.url = URI(self.url)

        if self.dateCreated is not None and not isinstance(self.dateCreated, XSDDate):
            self.dateCreated = XSDDate(self.dateCreated)

        if self.dateModified is not None and not isinstance(self.dateModified, XSDDate):
            self.dateModified = XSDDate(self.dateModified)

        if self.isDefinedByTaxonomy is not None and not isinstance(self.isDefinedByTaxonomy, TaxonomyId):
            self.isDefinedByTaxonomy = TaxonomyId(self.isDefinedByTaxonomy)

        if not isinstance(self.hasRule, list):
            self.hasRule = [self.hasRule] if self.hasRule is not None else []
        self.hasRule = [v if isinstance(v, RuleId) else RuleId(v) for v in self.hasRule]

        self.type = str(self.class_name)

        if self.hasControlApplication is not None and not isinstance(self.hasControlApplication, AIUC1ControlApplicationCategory):
            self.hasControlApplication = AIUC1ControlApplicationCategory(self.hasControlApplication)

        if not isinstance(self.hasEvidenceCategory, list):
            self.hasEvidenceCategory = [self.hasEvidenceCategory] if self.hasEvidenceCategory is not None else []
        self.hasEvidenceCategory = [v if isinstance(v, AIUC1EvidenceCategory) else AIUC1EvidenceCategory(v) for v in self.hasEvidenceCategory]

        if not isinstance(self.hasTypicalLocation, list):
            self.hasTypicalLocation = [self.hasTypicalLocation] if self.hasTypicalLocation is not None else []
        self.hasTypicalLocation = [v if isinstance(v, str) else str(v) for v in self.hasTypicalLocation]

        if not isinstance(self.appliesToCapability, list):
            self.appliesToCapability = [self.appliesToCapability] if self.appliesToCapability is not None else []
        self.appliesToCapability = [v if isinstance(v, AiTaskId) else AiTaskId(v) for v in self.appliesToCapability]

        if self.hasRequirement is not None and not isinstance(self.hasRequirement, RequirementId):
            self.hasRequirement = RequirementId(self.hasRequirement)

        if self.hasRequirementType is not None and not isinstance(self.hasRequirementType, AIUC1RequirementType):
            self.hasRequirementType = AIUC1RequirementType(self.hasRequirementType)

        if self.hasTypicalEvidence is not None and not isinstance(self.hasTypicalEvidence, str):
            self.hasTypicalEvidence = str(self.hasTypicalEvidence)

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class ControlActivityRecommendation(Recommendation):
    """
    A control activity (rule) describing a recommendation for performing an activity
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["ControlActivityRecommendation"]
    class_class_curie: ClassVar[str] = "nexus:ControlActivityRecommendation"
    class_name: ClassVar[str] = "ControlActivityRecommendation"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.ControlActivityRecommendation

    id: Union[str, ControlActivityRecommendationId] = None
    name: Optional[str] = None
    description: Optional[str] = None
    url: Optional[Union[str, URI]] = None
    dateCreated: Optional[Union[str, XSDDate]] = None
    dateModified: Optional[Union[str, XSDDate]] = None
    exact_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    close_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    related_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    broad_mappings: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    isCategorizedAs: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()
    isDefinedByTaxonomy: Optional[Union[str, TaxonomyId]] = None
    hasRule: Optional[Union[Union[str, RuleId], list[Union[str, RuleId]]]] = empty_list()
    type: Optional[str] = None
    hasControlApplication: Optional[Union[str, "AIUC1ControlApplicationCategory"]] = None
    hasEvidenceCategory: Optional[Union[Union[str, "AIUC1EvidenceCategory"], list[Union[str, "AIUC1EvidenceCategory"]]]] = empty_list()
    hasTypicalLocation: Optional[Union[str, list[str]]] = empty_list()
    appliesToCapability: Optional[Union[Union[str, AiTaskId], list[Union[str, AiTaskId]]]] = empty_list()
    hasRequirement: Optional[Union[str, RequirementId]] = None
    hasRequirementType: Optional[Union[str, "AIUC1RequirementType"]] = None
    hasTypicalEvidence: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ControlActivityRecommendationId):
            self.id = ControlActivityRecommendationId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.url is not None and not isinstance(self.url, URI):
            self.url = URI(self.url)

        if self.dateCreated is not None and not isinstance(self.dateCreated, XSDDate):
            self.dateCreated = XSDDate(self.dateCreated)

        if self.dateModified is not None and not isinstance(self.dateModified, XSDDate):
            self.dateModified = XSDDate(self.dateModified)

        if self.isDefinedByTaxonomy is not None and not isinstance(self.isDefinedByTaxonomy, TaxonomyId):
            self.isDefinedByTaxonomy = TaxonomyId(self.isDefinedByTaxonomy)

        if not isinstance(self.hasRule, list):
            self.hasRule = [self.hasRule] if self.hasRule is not None else []
        self.hasRule = [v if isinstance(v, RuleId) else RuleId(v) for v in self.hasRule]

        self.type = str(self.class_name)

        if self.hasControlApplication is not None and not isinstance(self.hasControlApplication, AIUC1ControlApplicationCategory):
            self.hasControlApplication = AIUC1ControlApplicationCategory(self.hasControlApplication)

        if not isinstance(self.hasEvidenceCategory, list):
            self.hasEvidenceCategory = [self.hasEvidenceCategory] if self.hasEvidenceCategory is not None else []
        self.hasEvidenceCategory = [v if isinstance(v, AIUC1EvidenceCategory) else AIUC1EvidenceCategory(v) for v in self.hasEvidenceCategory]

        if not isinstance(self.hasTypicalLocation, list):
            self.hasTypicalLocation = [self.hasTypicalLocation] if self.hasTypicalLocation is not None else []
        self.hasTypicalLocation = [v if isinstance(v, str) else str(v) for v in self.hasTypicalLocation]

        if not isinstance(self.appliesToCapability, list):
            self.appliesToCapability = [self.appliesToCapability] if self.appliesToCapability is not None else []
        self.appliesToCapability = [v if isinstance(v, AiTaskId) else AiTaskId(v) for v in self.appliesToCapability]

        if self.hasRequirement is not None and not isinstance(self.hasRequirement, RequirementId):
            self.hasRequirement = RequirementId(self.hasRequirement)

        if self.hasRequirementType is not None and not isinstance(self.hasRequirementType, AIUC1RequirementType):
            self.hasRequirementType = AIUC1RequirementType(self.hasRequirementType)

        if self.hasTypicalEvidence is not None and not isinstance(self.hasTypicalEvidence, str):
            self.hasTypicalEvidence = str(self.hasTypicalEvidence)

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class Requirement(Rule):
    """
    A requirement representing a combination of obligation, permission, or prohibition for AI system assurance.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NEXUS["Requirement"]
    class_class_curie: ClassVar[str] = "nexus:Requirement"
    class_name: ClassVar[str] = "Requirement"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.Requirement

    id: Union[str, RequirementId] = None
    hasApplication: Optional[Union[Union[str, "AIUC1ApplicationCategory"], list[Union[str, "AIUC1ApplicationCategory"]]]] = empty_list()
    hasFrequency: Optional[Union[str, "AIUC1Frequency"]] = None
    hasKeywords: Optional[Union[str, list[str]]] = empty_list()
    hasPrinciple: Optional[Union[Union[str, PrincipleId], list[Union[str, PrincipleId]]]] = empty_list()
    appliesToCapability: Optional[Union[Union[str, AiTaskId], list[Union[str, AiTaskId]]]] = empty_list()
    hasRequirementType: Optional[Union[str, "AIUC1RequirementType"]] = None
    isDefinedByTaxonomy: Optional[Union[str, TaxonomyId]] = None
    hasRule: Optional[Union[Union[str, RuleId], list[Union[str, RuleId]]]] = empty_list()
    type: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, RequirementId):
            self.id = RequirementId(self.id)

        if not isinstance(self.hasApplication, list):
            self.hasApplication = [self.hasApplication] if self.hasApplication is not None else []
        self.hasApplication = [v if isinstance(v, AIUC1ApplicationCategory) else AIUC1ApplicationCategory(v) for v in self.hasApplication]

        if self.hasFrequency is not None and not isinstance(self.hasFrequency, AIUC1Frequency):
            self.hasFrequency = AIUC1Frequency(self.hasFrequency)

        if not isinstance(self.hasKeywords, list):
            self.hasKeywords = [self.hasKeywords] if self.hasKeywords is not None else []
        self.hasKeywords = [v if isinstance(v, str) else str(v) for v in self.hasKeywords]

        if not isinstance(self.hasPrinciple, list):
            self.hasPrinciple = [self.hasPrinciple] if self.hasPrinciple is not None else []
        self.hasPrinciple = [v if isinstance(v, PrincipleId) else PrincipleId(v) for v in self.hasPrinciple]

        if not isinstance(self.appliesToCapability, list):
            self.appliesToCapability = [self.appliesToCapability] if self.appliesToCapability is not None else []
        self.appliesToCapability = [v if isinstance(v, AiTaskId) else AiTaskId(v) for v in self.appliesToCapability]

        if self.hasRequirementType is not None and not isinstance(self.hasRequirementType, AIUC1RequirementType):
            self.hasRequirementType = AIUC1RequirementType(self.hasRequirementType)

        if self.isDefinedByTaxonomy is not None and not isinstance(self.isDefinedByTaxonomy, TaxonomyId):
            self.isDefinedByTaxonomy = TaxonomyId(self.isDefinedByTaxonomy)

        if not isinstance(self.hasRule, list):
            self.hasRule = [self.hasRule] if self.hasRule is not None else []
        self.hasRule = [v if isinstance(v, RuleId) else RuleId(v) for v in self.hasRule]

        self.type = str(self.class_name)

        super().__post_init__(**kwargs)
        self.unknown_type = str(self.class_name)


@dataclass(repr=False)
class AiOffice(Organization):
    """
    The EU AI Office (https://digital-strategy.ec.europa.eu/en/policies/ai-office)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCHEMA["Organization"]
    class_class_curie: ClassVar[str] = "schema:Organization"
    class_name: ClassVar[str] = "AiOffice"
    class_model_uri: ClassVar[URIRef] = AI_GOVERNANCE_FRAMEWORK.AiOffice

    id: Union[str, AiOfficeId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AiOfficeId):
            self.id = AiOfficeId(self.id)

        super().__post_init__(**kwargs)


# Enumerations
class Jurisdiction(EnumDefinitionImpl):
    """
    A legal or political jurisdiction. Primary values are ISO 3166-1 alpha-2 country codes sourced from the DPV
    Location ontology (https://w3id.org/dpv/loc) as subclasses of dpv:Country. Additional permissible values cover
    supranational scopes (EU, INTL, GLOBAL) and long-form aliases used by FINOS source data (UK as alias for GB,
    International as alias for INTL). FINOS-LOCAL: the permissible_values extensions are awaiting upstream adoption
    (see ISSUE-nexus.md G29).
    """
    US = PermissibleValue(
        text="US",
        description="United States (ISO 3166-1 alpha-2).")
    UK = PermissibleValue(
        text="UK",
        description="United Kingdom — long-form alias for GB used by FINOS source data.")
    EU = PermissibleValue(
        text="EU",
        description="European Union (supranational scope).")
    International = PermissibleValue(
        text="International",
        description="International scope, transcending national borders (alias for INTL).")
    INTL = PermissibleValue(
        text="INTL",
        description="International scope, not bound to a single ISO 3166-1 country.")
    GLOBAL = PermissibleValue(
        text="GLOBAL",
        description="Global scope.")

    _defn = EnumDefinition(
        name="Jurisdiction",
        description="""A legal or political jurisdiction. Primary values are ISO 3166-1 alpha-2 country codes sourced from the DPV Location ontology (https://w3id.org/dpv/loc) as subclasses of dpv:Country. Additional permissible values cover supranational scopes (EU, INTL, GLOBAL) and long-form aliases used by FINOS source data (UK as alias for GB, International as alias for INTL). FINOS-LOCAL: the permissible_values extensions are awaiting upstream adoption (see ISSUE-nexus.md G29).""",
    )

class AdapterType(EnumDefinitionImpl):

    LORA = PermissibleValue(
        text="LORA",
        description="""Low-rank adapters, or LoRAs, are a fast way to give generalist large language models targeted knowledge and skills so they can do things like summarize IT manuals or rate the accuracy of their own answers. LoRA reduces the number of trainable parameters by learning pairs of rank-decompostion matrices while freezing the original weights. This vastly reduces the storage requirement for large language models adapted to specific tasks and enables efficient task-switching during deployment all without introducing inference latency. LoRA also outperforms several other adaptation methods including adapter, prefix-tuning, and fine-tuning. See arXiv:2106.09685""")
    ALORA = PermissibleValue(
        text="ALORA",
        description="""Activated LoRA (aLoRA) is a low rank adapter architecture that allows for reusing existing base model KV cache for more efficient inference, unlike standard LoRA models. As a result, aLoRA models can be quickly invoked as-needed for specialized tasks during (long) flows where the base model is primarily used, avoiding potentially expensive prefill costs in terms of latency, throughput, and GPU memory. See arXiv:2504.12397 for further details.""")

    _defn = EnumDefinition(
        name="AdapterType",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "X-LORA",
            PermissibleValue(
                text="X-LORA",
                description="""Mixture of LoRA Experts (X-LoRA) is a mixture of experts method for LoRA which works by using dense or sparse gating to dynamically activate LoRA experts."""))

class AIUC1ApplicationCategory(EnumDefinitionImpl):

    MANDATORY = PermissibleValue(
        text="MANDATORY",
        description="Mandatory")
    OPTIONAL = PermissibleValue(
        text="OPTIONAL",
        description="Optional")

    _defn = EnumDefinition(
        name="AIUC1ApplicationCategory",
    )

class AIUC1ControlApplicationCategory(EnumDefinitionImpl):

    CORE = PermissibleValue(
        text="CORE",
        description="Core Control")
    SUPPLEMENTAL = PermissibleValue(
        text="SUPPLEMENTAL",
        description="Supplemental Control")

    _defn = EnumDefinition(
        name="AIUC1ControlApplicationCategory",
    )

class AIUC1EvidenceCategory(EnumDefinitionImpl):

    TECHNICAL_IMPLEMENTATION = PermissibleValue(
        text="TECHNICAL_IMPLEMENTATION",
        description="Technical Implementation")
    LEGAL_POLICIES = PermissibleValue(
        text="LEGAL_POLICIES",
        description="Legal Policies")
    OPERATIONAL_PRACTICES = PermissibleValue(
        text="OPERATIONAL_PRACTICES",
        description="Operational Practices")
    THIRD_PARTY_EVALS = PermissibleValue(
        text="THIRD_PARTY_EVALS",
        description="Third-party Evals")

    _defn = EnumDefinition(
        name="AIUC1EvidenceCategory",
    )

class AIUC1Frequency(EnumDefinitionImpl):

    MONTHS_3 = PermissibleValue(
        text="MONTHS_3",
        description="Every 3 months")
    MONTHS_6 = PermissibleValue(
        text="MONTHS_6",
        description="Every 6 months")
    MONTHS_12 = PermissibleValue(
        text="MONTHS_12",
        description="Every 12 months")

    _defn = EnumDefinition(
        name="AIUC1Frequency",
    )

class AIUC1RequirementType(EnumDefinitionImpl):

    DETECTIVE = PermissibleValue(
        text="DETECTIVE",
        description="Detective")
    PREVENTATIVE = PermissibleValue(
        text="PREVENTATIVE",
        description="Preventative")

    _defn = EnumDefinition(
        name="AIUC1RequirementType",
    )

class EuAiRiskCategory(EnumDefinitionImpl):

    EXCLUDED = PermissibleValue(
        text="EXCLUDED",
        description="Excluded")
    PROHIBITED = PermissibleValue(
        text="PROHIBITED",
        description="Prohibited")
    HIGH_RISK_EXCEPTION = PermissibleValue(
        text="HIGH_RISK_EXCEPTION",
        description="High-Risk Exception")
    HIGH_RISK = PermissibleValue(
        text="HIGH_RISK",
        description="High Risk")
    LIMITED_OR_LOW_RISK = PermissibleValue(
        text="LIMITED_OR_LOW_RISK",
        description="Limited or Low Risk")

    _defn = EnumDefinition(
        name="EuAiRiskCategory",
    )

class AiSystemType(EnumDefinitionImpl):

    GPAI = PermissibleValue(
        text="GPAI",
        description="General-purpose AI (GPAI)")
    GPAI_OS = PermissibleValue(
        text="GPAI_OS",
        description="General-purpose AI (GPAI) models released under free and open-source licences")
    PROHIBITED = PermissibleValue(
        text="PROHIBITED",
        description="""Prohibited AI system due to unacceptable risk category (e.g. social scoring systems and manipulative AI).""")
    SCIENTIFIC_RD = PermissibleValue(
        text="SCIENTIFIC_RD",
        description="AI used for scientific research and development")
    MILITARY_SECURITY = PermissibleValue(
        text="MILITARY_SECURITY",
        description="AI used for military, defense and security purposes.")
    HIGH_RISK = PermissibleValue(
        text="HIGH_RISK",
        description="AI systems pursuant to Article 6(1)(2) Classification Rules for High-Risk AI Systems")

    _defn = EnumDefinition(
        name="AiSystemType",
    )

# Slots
class slots:
    pass

slots.id = Slot(uri=SCHEMA.identifier, name="id", curie=SCHEMA.curie('identifier'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.id, domain=None, range=URIRef)

slots.isDefinedByVocabulary = Slot(uri=SCHEMA.isPartOf, name="isDefinedByVocabulary", curie=SCHEMA.curie('isPartOf'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.isDefinedByVocabulary, domain=None, range=Optional[Union[str, VocabularyId]])

slots.name = Slot(uri=SCHEMA.name, name="name", curie=SCHEMA.curie('name'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.name, domain=None, range=Optional[str])

slots.description = Slot(uri=SCHEMA.description, name="description", curie=SCHEMA.curie('description'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.description, domain=None, range=Optional[str])

slots.url = Slot(uri=SCHEMA.url, name="url", curie=SCHEMA.curie('url'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.url, domain=None, range=Optional[Union[str, URI]])

slots.dateCreated = Slot(uri=SCHEMA.dateCreated, name="dateCreated", curie=SCHEMA.curie('dateCreated'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.dateCreated, domain=None, range=Optional[Union[str, XSDDate]])

slots.dateModified = Slot(uri=SCHEMA.dateModified, name="dateModified", curie=SCHEMA.curie('dateModified'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.dateModified, domain=None, range=Optional[Union[str, XSDDate]])

slots.version = Slot(uri=SCHEMA.version, name="version", curie=SCHEMA.curie('version'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.version, domain=None, range=Optional[str])

slots.hasDocumentation = Slot(uri=AIRO.hasDocumentation, name="hasDocumentation", curie=AIRO.curie('hasDocumentation'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasDocumentation, domain=None, range=Optional[Union[Union[str, DocumentationId], list[Union[str, DocumentationId]]]])

slots.hasLicense = Slot(uri=AIRO.hasLicense, name="hasLicense", curie=AIRO.curie('hasLicense'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasLicense, domain=None, range=Optional[Union[str, LicenseId]])

slots.isComposedOf = Slot(uri=NEXUS.isComposedOf, name="isComposedOf", curie=NEXUS.curie('isComposedOf'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.isComposedOf, domain=None, range=Optional[Union[str, list[str]]])

slots.hasDataset = Slot(uri=NEXUS.hasDataset, name="hasDataset", curie=NEXUS.curie('hasDataset'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasDataset, domain=None, range=Optional[Union[Union[str, DatasetId], list[Union[str, DatasetId]]]])

slots.producer = Slot(uri=NEXUS.producer, name="producer", curie=NEXUS.curie('producer'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.producer, domain=None, range=Optional[Union[str, OrganizationId]])

slots.provider = Slot(uri=SCHEMA.provider, name="provider", curie=SCHEMA.curie('provider'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.provider, domain=None, range=Optional[Union[str, OrganizationId]])

slots.grants_license = Slot(uri=NEXUS.grants_license, name="grants_license", curie=NEXUS.curie('grants_license'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.grants_license, domain=None, range=Optional[Union[str, LicenseId]])

slots.value = Slot(uri=NEXUS.value, name="value", curie=NEXUS.curie('value'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.value, domain=None, range=str)

slots.evidence = Slot(uri=NEXUS.evidence, name="evidence", curie=NEXUS.curie('evidence'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.evidence, domain=None, range=Optional[str])

slots.isPartOf = Slot(uri=SCHEMA.isPartOf, name="isPartOf", curie=SCHEMA.curie('isPartOf'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.isPartOf, domain=None, range=Optional[str])

slots.hasPart = Slot(uri=SKOS.member, name="hasPart", curie=SKOS.curie('member'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasPart, domain=None, range=Optional[Union[str, list[str]]])

slots.hasCapability = Slot(uri=TECH.hasCapability, name="hasCapability", curie=TECH.curie('hasCapability'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasCapability, domain=None, range=Optional[Union[Union[str, CapabilityId], list[Union[str, CapabilityId]]]])

slots.requiredByTask = Slot(uri=NEXUS.requiredByTask, name="requiredByTask", curie=NEXUS.curie('requiredByTask'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.requiredByTask, domain=Capability, range=Optional[Union[Union[str, AiTaskId], list[Union[str, AiTaskId]]]])

slots.requiresCapability = Slot(uri=NEXUS.requiresCapability, name="requiresCapability", curie=NEXUS.curie('requiresCapability'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.requiresCapability, domain=Any, range=Optional[Union[Union[str, CapabilityId], list[Union[str, CapabilityId]]]])

slots.implementedByAdapter = Slot(uri=NEXUS.implementedByAdapter, name="implementedByAdapter", curie=NEXUS.curie('implementedByAdapter'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.implementedByAdapter, domain=Any, range=Optional[Union[Union[dict, "Any"], list[Union[dict, "Any"]]]])

slots.implementsCapability = Slot(uri=NEXUS.implementsCapability, name="implementsCapability", curie=NEXUS.curie('implementsCapability'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.implementsCapability, domain=Any, range=Optional[Union[Union[str, CapabilityId], list[Union[str, CapabilityId]]]])

slots.hasTerm = Slot(uri=NEXUS.hasTerm, name="hasTerm", curie=NEXUS.curie('hasTerm'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasTerm, domain=None, range=Optional[Union[Union[str, TermId], list[Union[str, TermId]]]])

slots.hasRelatedTerm = Slot(uri=NEXUS.hasRelatedTerm, name="hasRelatedTerm", curie=NEXUS.curie('hasRelatedTerm'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasRelatedTerm, domain=Any, range=Optional[Union[Union[str, TermId], list[Union[str, TermId]]]])

slots.hasParentDefinition = Slot(uri=NEXUS.hasParentDefinition, name="hasParentDefinition", curie=NEXUS.curie('hasParentDefinition'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasParentDefinition, domain=None, range=Optional[Union[Union[str, TermId], list[Union[str, TermId]]]])

slots.hasSubDefinition = Slot(uri=NEXUS.hasSubDefinition, name="hasSubDefinition", curie=NEXUS.curie('hasSubDefinition'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasSubDefinition, domain=None, range=Optional[Union[Union[str, TermId], list[Union[str, TermId]]]])

slots.hasRule = Slot(uri=DPV.hasRule, name="hasRule", curie=DPV.curie('hasRule'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasRule, domain=None, range=Optional[Union[Union[str, RuleId], list[Union[str, RuleId]]]])

slots.hasReasonDenial = Slot(uri=NEXUS.hasReasonDenial, name="hasReasonDenial", curie=NEXUS.curie('hasReasonDenial'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasReasonDenial, domain=None, range=Optional[str])

slots.hasShortReplyType = Slot(uri=NEXUS.hasShortReplyType, name="hasShortReplyType", curie=NEXUS.curie('hasShortReplyType'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasShortReplyType, domain=None, range=Optional[str])

slots.hasException = Slot(uri=NEXUS.hasException, name="hasException", curie=NEXUS.curie('hasException'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasException, domain=None, range=Optional[str])

slots.isDefinedByTaxonomy = Slot(uri=SCHEMA.isPartOf, name="isDefinedByTaxonomy", curie=SCHEMA.curie('isPartOf'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.isDefinedByTaxonomy, domain=None, range=Optional[Union[str, TaxonomyId]])

slots.close_mappings = Slot(uri=SKOS.closeMatch, name="close_mappings", curie=SKOS.curie('closeMatch'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.close_mappings, domain=None, range=Optional[Union[Union[dict, Any], list[Union[dict, Any]]]])

slots.exact_mappings = Slot(uri=SKOS.exactMatch, name="exact_mappings", curie=SKOS.curie('exactMatch'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.exact_mappings, domain=None, range=Optional[Union[Union[dict, Any], list[Union[dict, Any]]]])

slots.broad_mappings = Slot(uri=SKOS.broadMatch, name="broad_mappings", curie=SKOS.curie('broadMatch'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.broad_mappings, domain=None, range=Optional[Union[Union[dict, Any], list[Union[dict, Any]]]])

slots.narrow_mappings = Slot(uri=SKOS.narrowMatch, name="narrow_mappings", curie=SKOS.curie('narrowMatch'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.narrow_mappings, domain=None, range=Optional[Union[Union[dict, Any], list[Union[dict, Any]]]])

slots.related_mappings = Slot(uri=SKOS.relatedMatch, name="related_mappings", curie=SKOS.curie('relatedMatch'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.related_mappings, domain=None, range=Optional[Union[Union[dict, Any], list[Union[dict, Any]]]])

slots.belongsToDomain = Slot(uri=SCHEMA.isPartOf, name="belongsToDomain", curie=SCHEMA.curie('isPartOf'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.belongsToDomain, domain=None, range=Optional[Union[dict, Any]])

slots.isCategorizedAs = Slot(uri=NEXUS.isCategorizedAs, name="isCategorizedAs", curie=NEXUS.curie('isCategorizedAs'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.isCategorizedAs, domain=None, range=Optional[Union[Union[dict, Any], list[Union[dict, Any]]]])

slots.isApplicableinLocality = Slot(uri=NEXUS.isApplicableinLocality, name="isApplicableinLocality", curie=NEXUS.curie('isApplicableinLocality'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.isApplicableinLocality, domain=None, range=Optional[Union[Union[str, LocalityOfUseId], list[Union[str, LocalityOfUseId]]]])

slots.hasJurisdiction = Slot(uri=DPV.hasJurisdiction, name="hasJurisdiction", curie=DPV.curie('hasJurisdiction'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasJurisdiction, domain=None, range=Optional[Union[Union[str, "Jurisdiction"], list[Union[str, "Jurisdiction"]]]])

slots.hasAiActorTask = Slot(uri=NEXUS.hasAiActorTask, name="hasAiActorTask", curie=NEXUS.curie('hasAiActorTask'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasAiActorTask, domain=None, range=Optional[Union[str, list[str]]])

slots.hasRelatedRisk = Slot(uri=NEXUS.hasRelatedRisk, name="hasRelatedRisk", curie=NEXUS.curie('hasRelatedRisk'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasRelatedRisk, domain=Any, range=Optional[Union[Union[str, RiskId], list[Union[str, RiskId]]]])

slots.hasRelatedAction = Slot(uri=NEXUS.hasRelatedAction, name="hasRelatedAction", curie=NEXUS.curie('hasRelatedAction'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasRelatedAction, domain=None, range=Optional[Union[Union[str, ActionId], list[Union[str, ActionId]]]])

slots.detectsRiskConcept = Slot(uri=NEXUS.detectsRiskConcept, name="detectsRiskConcept", curie=NEXUS.curie('detectsRiskConcept'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.detectsRiskConcept, domain=None, range=Optional[Union[Union[str, RiskConceptId], list[Union[str, RiskConceptId]]]])

slots.isDetectedBy = Slot(uri=NEXUS.isDetectedBy, name="isDetectedBy", curie=NEXUS.curie('isDetectedBy'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.isDetectedBy, domain=None, range=Optional[Union[Union[str, RiskControlId], list[Union[str, RiskControlId]]]])

slots.mitigatesRiskConcept = Slot(uri=NEXUS.mitigatesRiskConcept, name="mitigatesRiskConcept", curie=NEXUS.curie('mitigatesRiskConcept'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.mitigatesRiskConcept, domain=None, range=Optional[Union[Union[str, RiskConceptId], list[Union[str, RiskConceptId]]]])

slots.isMitigatedBy = Slot(uri=NEXUS.isMitigatedBy, name="isMitigatedBy", curie=NEXUS.curie('isMitigatedBy'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.isMitigatedBy, domain=None, range=Optional[Union[Union[str, RiskControlId], list[Union[str, RiskControlId]]]])

slots.hasStatus = Slot(uri=NEXUS.hasStatus, name="hasStatus", curie=NEXUS.curie('hasStatus'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasStatus, domain=None, range=Optional[Union[str, IncidentStatusId]])

slots.hasSeverity = Slot(uri=NEXUS.hasSeverity, name="hasSeverity", curie=NEXUS.curie('hasSeverity'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasSeverity, domain=None, range=Optional[Union[str, SeverityId]])

slots.hasLikelihood = Slot(uri=NEXUS.hasLikelihood, name="hasLikelihood", curie=NEXUS.curie('hasLikelihood'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasLikelihood, domain=None, range=Optional[Union[str, LikelihoodId]])

slots.hasImpactOn = Slot(uri=NEXUS.hasImpactOn, name="hasImpactOn", curie=NEXUS.curie('hasImpactOn'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasImpactOn, domain=None, range=Optional[Union[str, ImpactId]])

slots.hasConsequence = Slot(uri=NEXUS.hasConsequence, name="hasConsequence", curie=NEXUS.curie('hasConsequence'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasConsequence, domain=None, range=Optional[Union[str, ConsequenceId]])

slots.hasImpact = Slot(uri=NEXUS.hasImpact, name="hasImpact", curie=NEXUS.curie('hasImpact'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasImpact, domain=None, range=Optional[Union[str, ImpactId]])

slots.hasVariant = Slot(uri=NEXUS.hasVariant, name="hasVariant", curie=NEXUS.curie('hasVariant'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasVariant, domain=RiskIncident, range=Optional[Union[str, RiskIncidentId]])

slots.refersToRisk = Slot(uri=NEXUS.refersToRisk, name="refersToRisk", curie=NEXUS.curie('refersToRisk'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.refersToRisk, domain=RiskIncident, range=Optional[Union[Union[str, RiskId], list[Union[str, RiskId]]]])

slots.evaluatedByBenchmark = Slot(uri=NEXUS.evaluatedByBenchmark, name="evaluatedByBenchmark", curie=NEXUS.curie('evaluatedByBenchmark'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.evaluatedByBenchmark, domain=Capability, range=Optional[Union[Union[str, BenchmarkMetadataCardId], list[Union[str, BenchmarkMetadataCardId]]]])

slots.evaluatesCapability = Slot(uri=NEXUS.evaluatesCapability, name="evaluatesCapability", curie=NEXUS.curie('evaluatesCapability'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.evaluatesCapability, domain=BenchmarkMetadataCard, range=Optional[Union[Union[str, CapabilityId], list[Union[str, CapabilityId]]]])

slots.implementedByIntrinsic = Slot(uri=NEXUS.implementedByIntrinsic, name="implementedByIntrinsic", curie=NEXUS.curie('implementedByIntrinsic'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.implementedByIntrinsic, domain=None, range=Optional[Union[Union[str, LLMIntrinsicId], list[Union[str, LLMIntrinsicId]]]])

slots.possessedByAi = Slot(uri=TECH.hasCapability, name="possessedByAi", curie=TECH.curie('hasCapability'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.possessedByAi, domain=Capability, range=Optional[Union[Union[str, BaseAiId], list[Union[str, BaseAiId]]]])

slots.numParameters = Slot(uri=NEXUS.numParameters, name="numParameters", curie=NEXUS.curie('numParameters'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.numParameters, domain=None, range=Optional[int])

slots.numTrainingTokens = Slot(uri=NEXUS.numTrainingTokens, name="numTrainingTokens", curie=NEXUS.curie('numTrainingTokens'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.numTrainingTokens, domain=None, range=Optional[int])

slots.contextWindowSize = Slot(uri=NEXUS.contextWindowSize, name="contextWindowSize", curie=NEXUS.curie('contextWindowSize'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.contextWindowSize, domain=None, range=Optional[int])

slots.architecture = Slot(uri=NEXUS.architecture, name="architecture", curie=NEXUS.curie('architecture'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.architecture, domain=None, range=Optional[str])

slots.hasInputModality = Slot(uri=NEXUS.hasInputModality, name="hasInputModality", curie=NEXUS.curie('hasInputModality'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasInputModality, domain=None, range=Optional[Union[Union[str, ModalityId], list[Union[str, ModalityId]]]])

slots.hasOutputModality = Slot(uri=NEXUS.hasOutputModality, name="hasOutputModality", curie=NEXUS.curie('hasOutputModality'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasOutputModality, domain=None, range=Optional[Union[Union[str, ModalityId], list[Union[str, ModalityId]]]])

slots.hasPurpose = Slot(uri=AIRO.hasPurpose, name="hasPurpose", curie=AIRO.curie('hasPurpose'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasPurpose, domain=None, range=Optional[Union[Union[str, PurposeId], list[Union[str, PurposeId]]]])

slots.hasTrainingData = Slot(uri=AIRO.hasTrainingData, name="hasTrainingData", curie=AIRO.curie('hasTrainingData'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasTrainingData, domain=None, range=Optional[Union[Union[str, DatasetId], list[Union[str, DatasetId]]]])

slots.isAppliedWithinDomain = Slot(uri=AIRO.isAppliedWithinDomain, name="isAppliedWithinDomain", curie=AIRO.curie('isAppliedWithinDomain'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.isAppliedWithinDomain, domain=None, range=Optional[Union[Union[str, DomainId], list[Union[str, DomainId]]]])

slots.isDeployedBy = Slot(uri=AIRO.isDeployedBy, name="isDeployedBy", curie=AIRO.curie('isDeployedBy'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.isDeployedBy, domain=None, range=Optional[Union[str, AIDeployerId]])

slots.isDevelopedBy = Slot(uri=AIRO.isDevelopedBy, name="isDevelopedBy", curie=AIRO.curie('isDevelopedBy'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.isDevelopedBy, domain=None, range=Optional[Union[str, AIDeveloperId]])

slots.isProvidedBy = Slot(uri=AIRO.isProvidedBy, name="isProvidedBy", curie=AIRO.curie('isProvidedBy'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.isProvidedBy, domain=None, range=Optional[Union[str, AiProviderId]])

slots.isUsedBy = Slot(uri=AIRO.isUsedBy, name="isUsedBy", curie=AIRO.curie('isUsedBy'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.isUsedBy, domain=None, range=Optional[Union[str, AiProviderId]])

slots.isUsedWithinLocality = Slot(uri=AIRO.isUsedWithinLocality, name="isUsedWithinLocality", curie=AIRO.curie('isUsedWithinLocality'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.isUsedWithinLocality, domain=None, range=Optional[Union[Union[str, LocalityOfUseId], list[Union[str, LocalityOfUseId]]]])

slots.training_data_preprocessing = Slot(uri=NEXUS.training_data_preprocessing, name="training_data_preprocessing", curie=NEXUS.curie('training_data_preprocessing'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.training_data_preprocessing, domain=None, range=Optional[Union[Union[str, DataPreprocessingId], list[Union[str, DataPreprocessingId]]]])

slots.validated_by = Slot(uri=NEXUS.validated_by, name="validated_by", curie=NEXUS.curie('validated_by'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.validated_by, domain=None, range=Optional[Union[dict[Union[str, AiModelValidationId], Union[dict, AiModelValidation]], list[Union[dict, AiModelValidation]]]])

slots.performsTask = Slot(uri=NEXUS.performsTask, name="performsTask", curie=NEXUS.curie('performsTask'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.performsTask, domain=None, range=Optional[Union[Union[str, AiTaskId], list[Union[str, AiTaskId]]]])

slots.fine_tuning = Slot(uri=NEXUS.fine_tuning, name="fine_tuning", curie=NEXUS.curie('fine_tuning'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.fine_tuning, domain=None, range=Optional[str])

slots.supported_languages = Slot(uri=NEXUS.supported_languages, name="supported_languages", curie=NEXUS.curie('supported_languages'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.supported_languages, domain=None, range=Optional[Union[str, list[str]]])

slots.hasModelCard = Slot(uri=NEXUS.hasModelCard, name="hasModelCard", curie=NEXUS.curie('hasModelCard'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasModelCard, domain=None, range=Optional[Union[str, list[str]]])

slots.hasRiskControl = Slot(uri=AIRO.hasRiskControl, name="hasRiskControl", curie=AIRO.curie('hasRiskControl'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasRiskControl, domain=None, range=Optional[Union[Union[str, RiskControlId], list[Union[str, RiskControlId]]]])

slots.hasAIUser = Slot(uri=AIRO.hasAiUser, name="hasAIUser", curie=AIRO.curie('hasAiUser'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasAIUser, domain=None, range=Optional[Union[Union[str, AIUserId], list[Union[str, AIUserId]]]])

slots.hasStakeholder = Slot(uri=AIRO.hasStakeholder, name="hasStakeholder", curie=AIRO.curie('hasStakeholder'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasStakeholder, domain=None, range=Optional[Union[Union[str, StakeholderId], list[Union[str, StakeholderId]]]])

slots.hasAISubject = Slot(uri=AIRO.hasAISubject, name="hasAISubject", curie=AIRO.curie('hasAISubject'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasAISubject, domain=None, range=Optional[Union[Union[str, AISubjectId], list[Union[str, AISubjectId]]]])

slots.hasImplementation = Slot(uri=SCHEMA.url, name="hasImplementation", curie=SCHEMA.curie('url'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasImplementation, domain=None, range=Optional[Union[Union[str, URI], list[Union[str, URI]]]])

slots.hasUnitxtCard = Slot(uri=SCHEMA.url, name="hasUnitxtCard", curie=SCHEMA.curie('url'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasUnitxtCard, domain=None, range=Optional[Union[Union[str, URI], list[Union[str, URI]]]])

slots.hasBenchmarkMetadata = Slot(uri=NEXUS.hasBenchmarkMetadata, name="hasBenchmarkMetadata", curie=NEXUS.curie('hasBenchmarkMetadata'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasBenchmarkMetadata, domain=AiEval, range=Optional[Union[Union[str, BenchmarkMetadataCardId], list[Union[str, BenchmarkMetadataCardId]]]])

slots.describesAiEval = Slot(uri=NEXUS.describesAiEval, name="describesAiEval", curie=NEXUS.curie('describesAiEval'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.describesAiEval, domain=BenchmarkMetadataCard, range=Optional[Union[Union[str, AiEvalId], list[Union[str, AiEvalId]]]])

slots.bestValue = Slot(uri=NEXUS.bestValue, name="bestValue", curie=NEXUS.curie('bestValue'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.bestValue, domain=None, range=Optional[str])

slots.hasEvaluation = Slot(uri=DQV.hasQualityMeasurement, name="hasEvaluation", curie=DQV.curie('hasQualityMeasurement'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasEvaluation, domain=None, range=Optional[Union[Union[str, AiEvalResultId], list[Union[str, AiEvalResultId]]]])

slots.isResultOf = Slot(uri=DQV.isMeasurementOf, name="isResultOf", curie=DQV.curie('isMeasurementOf'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.isResultOf, domain=None, range=Optional[Union[str, AiEvalId]])

slots.hasDataType = Slot(uri=NEXUS.hasDataType, name="hasDataType", curie=NEXUS.curie('hasDataType'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasDataType, domain=None, range=Optional[Union[str, list[str]]])

slots.hasDomains = Slot(uri=NEXUS.hasDomains, name="hasDomains", curie=NEXUS.curie('hasDomains'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasDomains, domain=None, range=Optional[Union[str, list[str]]])

slots.hasLanguages = Slot(uri=NEXUS.hasLanguages, name="hasLanguages", curie=NEXUS.curie('hasLanguages'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasLanguages, domain=None, range=Optional[Union[str, list[str]]])

slots.hasSimilarBenchmarks = Slot(uri=NEXUS.hasSimilarBenchmarks, name="hasSimilarBenchmarks", curie=NEXUS.curie('hasSimilarBenchmarks'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasSimilarBenchmarks, domain=None, range=Optional[Union[str, list[str]]])

slots.hasResources = Slot(uri=NEXUS.hasResources, name="hasResources", curie=NEXUS.curie('hasResources'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasResources, domain=None, range=Optional[Union[str, list[str]]])

slots.hasGoal = Slot(uri=NEXUS.hasGoal, name="hasGoal", curie=NEXUS.curie('hasGoal'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasGoal, domain=None, range=Optional[str])

slots.hasAudience = Slot(uri=NEXUS.hasAudience, name="hasAudience", curie=NEXUS.curie('hasAudience'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasAudience, domain=None, range=Optional[Union[str, list[str]]])

slots.hasTasks = Slot(uri=NEXUS.hasTasks, name="hasTasks", curie=NEXUS.curie('hasTasks'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasTasks, domain=None, range=Optional[Union[str, list[str]]])

slots.hasLimitations = Slot(uri=NEXUS.hasLimitations, name="hasLimitations", curie=NEXUS.curie('hasLimitations'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasLimitations, domain=None, range=Optional[Union[str, list[str]]])

slots.hasOutOfScopeUses = Slot(uri=NEXUS.hasOutOfScopeUses, name="hasOutOfScopeUses", curie=NEXUS.curie('hasOutOfScopeUses'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasOutOfScopeUses, domain=None, range=Optional[Union[str, list[str]]])

slots.hasDataSource = Slot(uri=NEXUS.hasDataSource, name="hasDataSource", curie=NEXUS.curie('hasDataSource'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasDataSource, domain=None, range=Optional[Union[str, list[str]]])

slots.hasDataSize = Slot(uri=NEXUS.hasDataSize, name="hasDataSize", curie=NEXUS.curie('hasDataSize'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasDataSize, domain=None, range=Optional[str])

slots.hasDataFormat = Slot(uri=NEXUS.hasDataFormat, name="hasDataFormat", curie=NEXUS.curie('hasDataFormat'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasDataFormat, domain=None, range=Optional[Union[str, list[str]]])

slots.hasAnnotation = Slot(uri=NEXUS.hasAnnotation, name="hasAnnotation", curie=NEXUS.curie('hasAnnotation'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasAnnotation, domain=None, range=Optional[Union[str, list[str]]])

slots.hasMethods = Slot(uri=NEXUS.hasMethods, name="hasMethods", curie=NEXUS.curie('hasMethods'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasMethods, domain=None, range=Optional[Union[str, list[str]]])

slots.hasMetrics = Slot(uri=NEXUS.hasMetrics, name="hasMetrics", curie=NEXUS.curie('hasMetrics'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasMetrics, domain=None, range=Optional[Union[str, list[str]]])

slots.hasCalculation = Slot(uri=NEXUS.hasCalculation, name="hasCalculation", curie=NEXUS.curie('hasCalculation'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasCalculation, domain=None, range=Optional[Union[str, list[str]]])

slots.hasInterpretation = Slot(uri=NEXUS.hasInterpretation, name="hasInterpretation", curie=NEXUS.curie('hasInterpretation'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasInterpretation, domain=None, range=Optional[Union[str, list[str]]])

slots.hasBaselineResults = Slot(uri=NEXUS.hasBaselineResults, name="hasBaselineResults", curie=NEXUS.curie('hasBaselineResults'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasBaselineResults, domain=None, range=Optional[Union[str, list[str]]])

slots.hasValidation = Slot(uri=NEXUS.hasValidation, name="hasValidation", curie=NEXUS.curie('hasValidation'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasValidation, domain=None, range=Optional[Union[str, list[str]]])

slots.hasDemographicAnalysis = Slot(uri=NEXUS.hasDemographicAnalysis, name="hasDemographicAnalysis", curie=NEXUS.curie('hasDemographicAnalysis'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasDemographicAnalysis, domain=None, range=Optional[Union[str, list[str]]])

slots.hasConsiderationPrivacyAndAnonymity = Slot(uri=NEXUS.hasConsiderationPrivacyAndAnonymity, name="hasConsiderationPrivacyAndAnonymity", curie=NEXUS.curie('hasConsiderationPrivacyAndAnonymity'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasConsiderationPrivacyAndAnonymity, domain=None, range=Optional[Union[str, list[str]]])

slots.hasConsiderationConsentProcedures = Slot(uri=NEXUS.hasConsiderationConsentProcedures, name="hasConsiderationConsentProcedures", curie=NEXUS.curie('hasConsiderationConsentProcedures'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasConsiderationConsentProcedures, domain=None, range=Optional[Union[str, list[str]]])

slots.hasConsiderationComplianceWithRegulations = Slot(uri=NEXUS.hasConsiderationComplianceWithRegulations, name="hasConsiderationComplianceWithRegulations", curie=NEXUS.curie('hasConsiderationComplianceWithRegulations'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasConsiderationComplianceWithRegulations, domain=None, range=Optional[Union[str, list[str]]])

slots.hasSourceMetadata = Slot(uri=NEXUS.hasSourceMetadata, name="hasSourceMetadata", curie=NEXUS.curie('hasSourceMetadata'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasSourceMetadata, domain=EveryEvalAIResult, range=Optional[Union[dict, SourceMetadata]])

slots.hasModelInfo = Slot(uri=NEXUS.hasModelInfo, name="hasModelInfo", curie=NEXUS.curie('hasModelInfo'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasModelInfo, domain=EveryEvalAIResult, range=Optional[Union[dict, ModelInfo]])

slots.hasSourceData = Slot(uri=NEXUS.hasSourceData, name="hasSourceData", curie=NEXUS.curie('hasSourceData'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasSourceData, domain=EvaluationResultRecord, range=Optional[Union[dict, SourceData]])

slots.hasMetricConfig = Slot(uri=NEXUS.hasMetricConfig, name="hasMetricConfig", curie=NEXUS.curie('hasMetricConfig'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasMetricConfig, domain=EvaluationResultRecord, range=Optional[Union[dict, MetricConfig]])

slots.hasScoreDetails = Slot(uri=NEXUS.hasScoreDetails, name="hasScoreDetails", curie=NEXUS.curie('hasScoreDetails'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasScoreDetails, domain=EvaluationResultRecord, range=Optional[Union[dict, ScoreDetails]])

slots.hasEvaluationResults = Slot(uri=NEXUS.hasEvaluationResults, name="hasEvaluationResults", curie=NEXUS.curie('hasEvaluationResults'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasEvaluationResults, domain=EveryEvalAIResult, range=Optional[Union[dict[Union[str, EvaluationResultRecordId], Union[dict, EvaluationResultRecord]], list[Union[dict, EvaluationResultRecord]]]])

slots.hasAdapter = Slot(uri=NEXUS.hasAdapter, name="hasAdapter", curie=NEXUS.curie('hasAdapter'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasAdapter, domain=LLMIntrinsic, range=Optional[Union[Union[str, AdapterId], list[Union[str, AdapterId]]]])

slots.hasAdapterType = Slot(uri=NEXUS.hasAdapterType, name="hasAdapterType", curie=NEXUS.curie('hasAdapterType'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasAdapterType, domain=None, range=Optional[Union[Union[str, "AdapterType"], list[Union[str, "AdapterType"]]]])

slots.adaptsModel = Slot(uri=NEXUS.adaptsModel, name="adaptsModel", curie=NEXUS.curie('adaptsModel'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.adaptsModel, domain=None, range=Optional[Union[Union[str, LargeLanguageModelId], list[Union[str, LargeLanguageModelId]]]])

slots.hasApplication = Slot(uri=NEXUS.hasApplication, name="hasApplication", curie=NEXUS.curie('hasApplication'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasApplication, domain=Requirement, range=Optional[Union[Union[str, "AIUC1ApplicationCategory"], list[Union[str, "AIUC1ApplicationCategory"]]]])

slots.hasFrequency = Slot(uri=NEXUS.hasFrequency, name="hasFrequency", curie=NEXUS.curie('hasFrequency'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasFrequency, domain=Requirement, range=Optional[Union[str, "AIUC1Frequency"]])

slots.hasKeywords = Slot(uri=NEXUS.hasKeywords, name="hasKeywords", curie=NEXUS.curie('hasKeywords'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasKeywords, domain=Requirement, range=Optional[Union[str, list[str]]])

slots.hasPrinciple = Slot(uri=DPV.isPartOf, name="hasPrinciple", curie=DPV.curie('isPartOf'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasPrinciple, domain=Requirement, range=Optional[Union[Union[str, PrincipleId], list[Union[str, PrincipleId]]]])

slots.hasRequirementType = Slot(uri=NEXUS.hasRequirementType, name="hasRequirementType", curie=NEXUS.curie('hasRequirementType'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasRequirementType, domain=Any, range=Optional[Union[str, "AIUC1RequirementType"]])

slots.hasControlApplication = Slot(uri=NEXUS.hasControlApplication, name="hasControlApplication", curie=NEXUS.curie('hasControlApplication'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasControlApplication, domain=None, range=Optional[Union[str, "AIUC1ControlApplicationCategory"]])

slots.hasEvidenceCategory = Slot(uri=NEXUS.hasEvidenceCategory, name="hasEvidenceCategory", curie=NEXUS.curie('hasEvidenceCategory'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasEvidenceCategory, domain=None, range=Optional[Union[Union[str, "AIUC1EvidenceCategory"], list[Union[str, "AIUC1EvidenceCategory"]]]])

slots.hasTypicalLocation = Slot(uri=NEXUS.hasTypicalLocation, name="hasTypicalLocation", curie=NEXUS.curie('hasTypicalLocation'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasTypicalLocation, domain=None, range=Optional[Union[str, list[str]]])

slots.hasTypicalEvidence = Slot(uri=NEXUS.hasTypicalEvidence, name="hasTypicalEvidence", curie=NEXUS.curie('hasTypicalEvidence'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasTypicalEvidence, domain=None, range=Optional[str])

slots.appliesToCapability = Slot(uri=NEXUS.appliesToCapability, name="appliesToCapability", curie=NEXUS.curie('appliesToCapability'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.appliesToCapability, domain=None, range=Optional[Union[Union[str, AiTaskId], list[Union[str, AiTaskId]]]])

slots.hasRequirement = Slot(uri=NEXUS.hasRequirement, name="hasRequirement", curie=NEXUS.curie('hasRequirement'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasRequirement, domain=None, range=Optional[Union[str, RequirementId]])

slots.gpu_hours = Slot(uri=NEXUS.gpu_hours, name="gpu_hours", curie=NEXUS.curie('gpu_hours'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.gpu_hours, domain=None, range=Optional[int])

slots.power_consumption_w = Slot(uri=NEXUS.power_consumption_w, name="power_consumption_w", curie=NEXUS.curie('power_consumption_w'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.power_consumption_w, domain=None, range=Optional[int])

slots.carbon_emitted = Slot(uri=NEXUS.carbon_emitted, name="carbon_emitted", curie=NEXUS.curie('carbon_emitted'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.carbon_emitted, domain=None, range=Optional[float])

slots.isImportedBy = Slot(uri=NEXUS.isImportedBy, name="isImportedBy", curie=NEXUS.curie('isImportedBy'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.isImportedBy, domain=None, range=Optional[Union[dict, Organization]])

slots.isDistributedBy = Slot(uri=NEXUS.isDistributedBy, name="isDistributedBy", curie=NEXUS.curie('isDistributedBy'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.isDistributedBy, domain=None, range=Optional[Union[dict, Organization]])

slots.hasEuAiSystemType = Slot(uri=NEXUS.hasEuAiSystemType, name="hasEuAiSystemType", curie=NEXUS.curie('hasEuAiSystemType'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasEuAiSystemType, domain=None, range=Optional[Union[str, "AiSystemType"]])

slots.hasEuRiskCategory = Slot(uri=NEXUS.hasEuRiskCategory, name="hasEuRiskCategory", curie=NEXUS.curie('hasEuRiskCategory'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.hasEuRiskCategory, domain=None, range=Optional[Union[str, "EuAiRiskCategory"]])

slots.container__organizations = Slot(uri=NEXUS.organizations, name="container__organizations", curie=NEXUS.curie('organizations'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.container__organizations, domain=None, range=Optional[Union[dict[Union[str, OrganizationId], Union[dict, Organization]], list[Union[dict, Organization]]]])

slots.container__licenses = Slot(uri=NEXUS.licenses, name="container__licenses", curie=NEXUS.curie('licenses'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.container__licenses, domain=None, range=Optional[Union[dict[Union[str, LicenseId], Union[dict, License]], list[Union[dict, License]]]])

slots.container__modalities = Slot(uri=NEXUS.modalities, name="container__modalities", curie=NEXUS.curie('modalities'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.container__modalities, domain=None, range=Optional[Union[dict[Union[str, ModalityId], Union[dict, Modality]], list[Union[dict, Modality]]]])

slots.container__aitasks = Slot(uri=NEXUS.aitasks, name="container__aitasks", curie=NEXUS.curie('aitasks'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.container__aitasks, domain=None, range=Optional[Union[dict[Union[str, AiTaskId], Union[dict, AiTask]], list[Union[dict, AiTask]]]])

slots.container__documents = Slot(uri=NEXUS.documents, name="container__documents", curie=NEXUS.curie('documents'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.container__documents, domain=None, range=Optional[Union[dict[Union[str, DocumentationId], Union[dict, Documentation]], list[Union[dict, Documentation]]]])

slots.container__datasets = Slot(uri=NEXUS.datasets, name="container__datasets", curie=NEXUS.curie('datasets'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.container__datasets, domain=None, range=Optional[Union[dict[Union[str, DatasetId], Union[dict, Dataset]], list[Union[dict, Dataset]]]])

slots.container__llmintrinsics = Slot(uri=NEXUS.llmintrinsics, name="container__llmintrinsics", curie=NEXUS.curie('llmintrinsics'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.container__llmintrinsics, domain=None, range=Optional[Union[dict[Union[str, LLMIntrinsicId], Union[dict, LLMIntrinsic]], list[Union[dict, LLMIntrinsic]]]])

slots.container__adapters = Slot(uri=NEXUS.adapters, name="container__adapters", curie=NEXUS.curie('adapters'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.container__adapters, domain=None, range=Optional[Union[dict[Union[str, AdapterId], Union[dict, Adapter]], list[Union[dict, Adapter]]]])

slots.container__taxonomies = Slot(uri=NEXUS.taxonomies, name="container__taxonomies", curie=NEXUS.curie('taxonomies'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.container__taxonomies, domain=None, range=Optional[Union[dict[Union[str, TaxonomyId], Union[dict, Taxonomy]], list[Union[dict, Taxonomy]]]])

slots.container__concepts = Slot(uri=NEXUS.concepts, name="container__concepts", curie=NEXUS.curie('concepts'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.container__concepts, domain=None, range=Optional[Union[dict[Union[str, ConceptId], Union[dict, Concept]], list[Union[dict, Concept]]]])

slots.container__entries = Slot(uri=NEXUS.entries, name="container__entries", curie=NEXUS.curie('entries'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.container__entries, domain=None, range=Optional[Union[dict[Union[str, EntryId], Union[dict, Entry]], list[Union[dict, Entry]]]])

slots.container__groups = Slot(uri=NEXUS.groups, name="container__groups", curie=NEXUS.curie('groups'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.container__groups, domain=None, range=Optional[Union[dict[Union[str, GroupId], Union[dict, Group]], list[Union[dict, Group]]]])

slots.container__vocabularies = Slot(uri=NEXUS.vocabularies, name="container__vocabularies", curie=NEXUS.curie('vocabularies'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.container__vocabularies, domain=None, range=Optional[Union[dict[Union[str, VocabularyId], Union[dict, Vocabulary]], list[Union[dict, Vocabulary]]]])

slots.container__controls = Slot(uri=NEXUS.controls, name="container__controls", curie=NEXUS.curie('controls'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.container__controls, domain=None, range=Optional[Union[dict[Union[str, ControlId], Union[dict, Control]], list[Union[dict, Control]]]])

slots.container__riskincidents = Slot(uri=NEXUS.riskincidents, name="container__riskincidents", curie=NEXUS.curie('riskincidents'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.container__riskincidents, domain=None, range=Optional[Union[dict[Union[str, RiskIncidentId], Union[dict, RiskIncident]], list[Union[dict, RiskIncident]]]])

slots.container__stakeholdergroups = Slot(uri=NEXUS.stakeholdergroups, name="container__stakeholdergroups", curie=NEXUS.curie('stakeholdergroups'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.container__stakeholdergroups, domain=None, range=Optional[Union[dict[Union[str, StakeholderGroupId], Union[dict, StakeholderGroup]], list[Union[dict, StakeholderGroup]]]])

slots.container__stakeholders = Slot(uri=NEXUS.stakeholders, name="container__stakeholders", curie=NEXUS.curie('stakeholders'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.container__stakeholders, domain=None, range=Optional[Union[dict[Union[str, StakeholderId], Union[dict, Stakeholder]], list[Union[dict, Stakeholder]]]])

slots.container__actions = Slot(uri=NEXUS.actions, name="container__actions", curie=NEXUS.curie('actions'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.container__actions, domain=None, range=Optional[Union[dict[Union[str, ActionId], Union[dict, Action]], list[Union[dict, Action]]]])

slots.container__evaluations = Slot(uri=NEXUS.evaluations, name="container__evaluations", curie=NEXUS.curie('evaluations'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.container__evaluations, domain=None, range=Optional[Union[dict[Union[str, AiEvalId], Union[dict, AiEval]], list[Union[dict, AiEval]]]])

slots.container__aievalresults = Slot(uri=NEXUS.aievalresults, name="container__aievalresults", curie=NEXUS.curie('aievalresults'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.container__aievalresults, domain=None, range=Optional[Union[dict[Union[str, AiEvalResultId], Union[dict, AiEvalResult]], list[Union[dict, AiEvalResult]]]])

slots.container__benchmarkmetadatacards = Slot(uri=NEXUS.benchmarkmetadatacards, name="container__benchmarkmetadatacards", curie=NEXUS.curie('benchmarkmetadatacards'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.container__benchmarkmetadatacards, domain=None, range=Optional[Union[dict[Union[str, BenchmarkMetadataCardId], Union[dict, BenchmarkMetadataCard]], list[Union[dict, BenchmarkMetadataCard]]]])

slots.container__aimodelfamilies = Slot(uri=NEXUS.aimodelfamilies, name="container__aimodelfamilies", curie=NEXUS.curie('aimodelfamilies'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.container__aimodelfamilies, domain=None, range=Optional[Union[dict[Union[str, LargeLanguageModelFamilyId], Union[dict, LargeLanguageModelFamily]], list[Union[dict, LargeLanguageModelFamily]]]])

slots.container__aimodels = Slot(uri=NEXUS.aimodels, name="container__aimodels", curie=NEXUS.curie('aimodels'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.container__aimodels, domain=None, range=Optional[Union[dict[Union[str, LargeLanguageModelId], Union[dict, LargeLanguageModel]], list[Union[dict, LargeLanguageModel]]]])

slots.container__policies = Slot(uri=NEXUS.policies, name="container__policies", curie=NEXUS.curie('policies'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.container__policies, domain=None, range=Optional[Union[dict[Union[str, PolicyId], Union[dict, Policy]], list[Union[dict, Policy]]]])

slots.container__rules = Slot(uri=NEXUS.rules, name="container__rules", curie=NEXUS.curie('rules'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.container__rules, domain=None, range=Optional[Union[dict[Union[str, RuleId], Union[dict, Rule]], list[Union[dict, Rule]]]])

slots.container__prohibitions = Slot(uri=NEXUS.prohibitions, name="container__prohibitions", curie=NEXUS.curie('prohibitions'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.container__prohibitions, domain=None, range=Optional[Union[dict[Union[str, ProhibitionId], Union[dict, Prohibition]], list[Union[dict, Prohibition]]]])

slots.container__permissions = Slot(uri=NEXUS.permissions, name="container__permissions", curie=NEXUS.curie('permissions'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.container__permissions, domain=None, range=Optional[Union[dict[Union[str, PermissionId], Union[dict, Permission]], list[Union[dict, Permission]]]])

slots.container__obligations = Slot(uri=NEXUS.obligations, name="container__obligations", curie=NEXUS.curie('obligations'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.container__obligations, domain=None, range=Optional[Union[dict[Union[str, ObligationId], Union[dict, Obligation]], list[Union[dict, Obligation]]]])

slots.documentation__author = Slot(uri=NEXUS.author, name="documentation__author", curie=NEXUS.curie('author'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.documentation__author, domain=None, range=Optional[str])

slots.vocabulary__type = Slot(uri=NEXUS.type, name="vocabulary__type", curie=NEXUS.curie('type'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.vocabulary__type, domain=None, range=Optional[str])

slots.taxonomy__type = Slot(uri=NEXUS.type, name="taxonomy__type", curie=NEXUS.curie('type'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.taxonomy__type, domain=None, range=Optional[str])

slots.concept__type = Slot(uri=NEXUS.type, name="concept__type", curie=NEXUS.curie('type'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.concept__type, domain=None, range=Optional[str])

slots.control__type = Slot(uri=NEXUS.type, name="control__type", curie=NEXUS.curie('type'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.control__type, domain=None, range=Optional[str])

slots.group__type = Slot(uri=NEXUS.type, name="group__type", curie=NEXUS.curie('type'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.group__type, domain=None, range=Optional[str])

slots.group__narrower = Slot(uri=SKOS.narrower, name="group__narrower", curie=SKOS.curie('narrower'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.group__narrower, domain=None, range=Optional[Union[str, list[str]]])

slots.group__broader = Slot(uri=SKOS.narrower, name="group__broader", curie=SKOS.curie('narrower'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.group__broader, domain=None, range=Optional[Union[str, list[str]]])

slots.entry__type = Slot(uri=NEXUS.type, name="entry__type", curie=NEXUS.curie('type'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.entry__type, domain=None, range=Optional[str])

slots.policy__type = Slot(uri=NEXUS.type, name="policy__type", curie=NEXUS.curie('type'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.policy__type, domain=None, range=Optional[str])

slots.rule__type = Slot(uri=NEXUS.type, name="rule__type", curie=NEXUS.curie('type'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.rule__type, domain=None, range=Optional[str])

slots.attributeConditionRule__preconditions = Slot(uri=NEXUS.preconditions, name="attributeConditionRule__preconditions", curie=NEXUS.curie('preconditions'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.attributeConditionRule__preconditions, domain=None, range=Optional[Union[dict, AnonymousClassExpression]])

slots.attributeConditionRule__postconditions = Slot(uri=NEXUS.postconditions, name="attributeConditionRule__postconditions", curie=NEXUS.curie('postconditions'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.attributeConditionRule__postconditions, domain=None, range=Optional[Union[dict, AnonymousClassExpression]])

slots.anonymousClassExpression__slot_conditions = Slot(uri=NEXUS.slot_conditions, name="anonymousClassExpression__slot_conditions", curie=NEXUS.curie('slot_conditions'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.anonymousClassExpression__slot_conditions, domain=None, range=Optional[Union[Union[dict, SlotCondition], list[Union[dict, SlotCondition]]]])

slots.slotCondition__slot_name = Slot(uri=NEXUS.slot_name, name="slotCondition__slot_name", curie=NEXUS.curie('slot_name'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.slotCondition__slot_name, domain=None, range=Optional[str])

slots.slotCondition__equals_string = Slot(uri=NEXUS.equals_string, name="slotCondition__equals_string", curie=NEXUS.curie('equals_string'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.slotCondition__equals_string, domain=None, range=Optional[str])

slots.permission__type = Slot(uri=NEXUS.type, name="permission__type", curie=NEXUS.curie('type'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.permission__type, domain=None, range=Optional[str])

slots.prohibition__type = Slot(uri=NEXUS.type, name="prohibition__type", curie=NEXUS.curie('type'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.prohibition__type, domain=None, range=Optional[str])

slots.obligation__type = Slot(uri=NEXUS.type, name="obligation__type", curie=NEXUS.curie('type'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.obligation__type, domain=None, range=Optional[str])

slots.recommendation__type = Slot(uri=NEXUS.type, name="recommendation__type", curie=NEXUS.curie('type'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.recommendation__type, domain=None, range=Optional[str])

slots.certification__type = Slot(uri=NEXUS.type, name="certification__type", curie=NEXUS.curie('type'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.certification__type, domain=None, range=Optional[str])

slots.risk__tag = Slot(uri=NEXUS.tag, name="risk__tag", curie=NEXUS.curie('tag'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.risk__tag, domain=None, range=Optional[str])

slots.risk__risk_type = Slot(uri=NEXUS.risk_type, name="risk__risk_type", curie=NEXUS.curie('risk_type'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.risk__risk_type, domain=None, range=Optional[str])

slots.risk__phase = Slot(uri=NEXUS.phase, name="risk__phase", curie=NEXUS.curie('phase'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.risk__phase, domain=None, range=Optional[str])

slots.risk__descriptor = Slot(uri=NEXUS.descriptor, name="risk__descriptor", curie=NEXUS.curie('descriptor'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.risk__descriptor, domain=None, range=Optional[Union[str, list[str]]])

slots.risk__concern = Slot(uri=NEXUS.concern, name="risk__concern", curie=NEXUS.curie('concern'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.risk__concern, domain=None, range=Optional[str])

slots.riskIncident__author = Slot(uri=NEXUS.author, name="riskIncident__author", curie=NEXUS.curie('author'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.riskIncident__author, domain=None, range=Optional[str])

slots.riskIncident__source_uri = Slot(uri=NEXUS.source_uri, name="riskIncident__source_uri", curie=NEXUS.curie('source_uri'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.riskIncident__source_uri, domain=None, range=Optional[str])

slots.sourceMetadata__source_name = Slot(uri=NEXUS.source_name, name="sourceMetadata__source_name", curie=NEXUS.curie('source_name'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.sourceMetadata__source_name, domain=None, range=Optional[str])

slots.sourceMetadata__source_type = Slot(uri=NEXUS.source_type, name="sourceMetadata__source_type", curie=NEXUS.curie('source_type'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.sourceMetadata__source_type, domain=None, range=Optional[str])

slots.sourceMetadata__source_organization_name = Slot(uri=NEXUS.source_organization_name, name="sourceMetadata__source_organization_name", curie=NEXUS.curie('source_organization_name'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.sourceMetadata__source_organization_name, domain=None, range=Optional[str])

slots.sourceMetadata__source_organization_url = Slot(uri=NEXUS.source_organization_url, name="sourceMetadata__source_organization_url", curie=NEXUS.curie('source_organization_url'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.sourceMetadata__source_organization_url, domain=None, range=Optional[Union[str, URI]])

slots.sourceMetadata__evaluator_relationship = Slot(uri=NEXUS.evaluator_relationship, name="sourceMetadata__evaluator_relationship", curie=NEXUS.curie('evaluator_relationship'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.sourceMetadata__evaluator_relationship, domain=None, range=Optional[str])

slots.modelInfo__model_name = Slot(uri=NEXUS.model_name, name="modelInfo__model_name", curie=NEXUS.curie('model_name'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.modelInfo__model_name, domain=None, range=Optional[str])

slots.modelInfo__model_id = Slot(uri=NEXUS.model_id, name="modelInfo__model_id", curie=NEXUS.curie('model_id'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.modelInfo__model_id, domain=None, range=Optional[str])

slots.sourceData__dataset_name = Slot(uri=NEXUS.dataset_name, name="sourceData__dataset_name", curie=NEXUS.curie('dataset_name'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.sourceData__dataset_name, domain=None, range=Optional[str])

slots.sourceData__source_type = Slot(uri=NEXUS.source_type, name="sourceData__source_type", curie=NEXUS.curie('source_type'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.sourceData__source_type, domain=None, range=Optional[str])

slots.sourceData__hf_repo = Slot(uri=NEXUS.hf_repo, name="sourceData__hf_repo", curie=NEXUS.curie('hf_repo'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.sourceData__hf_repo, domain=None, range=Optional[str])

slots.sourceData__hf_split = Slot(uri=NEXUS.hf_split, name="sourceData__hf_split", curie=NEXUS.curie('hf_split'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.sourceData__hf_split, domain=None, range=Optional[str])

slots.metricConfig__lower_is_better = Slot(uri=NEXUS.lower_is_better, name="metricConfig__lower_is_better", curie=NEXUS.curie('lower_is_better'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.metricConfig__lower_is_better, domain=None, range=Optional[Union[bool, Bool]])

slots.metricConfig__score_type = Slot(uri=NEXUS.score_type, name="metricConfig__score_type", curie=NEXUS.curie('score_type'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.metricConfig__score_type, domain=None, range=Optional[str])

slots.metricConfig__min_score = Slot(uri=NEXUS.min_score, name="metricConfig__min_score", curie=NEXUS.curie('min_score'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.metricConfig__min_score, domain=None, range=Optional[float])

slots.metricConfig__max_score = Slot(uri=NEXUS.max_score, name="metricConfig__max_score", curie=NEXUS.curie('max_score'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.metricConfig__max_score, domain=None, range=Optional[float])

slots.scoreDetails__score = Slot(uri=NEXUS.score, name="scoreDetails__score", curie=NEXUS.curie('score'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.scoreDetails__score, domain=None, range=Optional[float])

slots.evaluationResultRecord__evaluation_name = Slot(uri=NEXUS.evaluation_name, name="evaluationResultRecord__evaluation_name", curie=NEXUS.curie('evaluation_name'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.evaluationResultRecord__evaluation_name, domain=None, range=Optional[str])

slots.everyEvalAIResult__schema_version = Slot(uri=NEXUS.schema_version, name="everyEvalAIResult__schema_version", curie=NEXUS.curie('schema_version'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.everyEvalAIResult__schema_version, domain=None, range=Optional[str])

slots.everyEvalAIResult__evaluation_id = Slot(uri=NEXUS.evaluation_id, name="everyEvalAIResult__evaluation_id", curie=NEXUS.curie('evaluation_id'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.everyEvalAIResult__evaluation_id, domain=None, range=Optional[str])

slots.everyEvalAIResult__evaluation_timestamp = Slot(uri=NEXUS.evaluation_timestamp, name="everyEvalAIResult__evaluation_timestamp", curie=NEXUS.curie('evaluation_timestamp'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.everyEvalAIResult__evaluation_timestamp, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.everyEvalAIResult__retrieved_timestamp = Slot(uri=NEXUS.retrieved_timestamp, name="everyEvalAIResult__retrieved_timestamp", curie=NEXUS.curie('retrieved_timestamp'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.everyEvalAIResult__retrieved_timestamp, domain=None, range=Optional[str])

slots.benchmarkMetadataCard__name = Slot(uri=NEXUS.name, name="benchmarkMetadataCard__name", curie=NEXUS.curie('name'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.benchmarkMetadataCard__name, domain=None, range=Optional[str])

slots.benchmarkMetadataCard__overview = Slot(uri=NEXUS.overview, name="benchmarkMetadataCard__overview", curie=NEXUS.curie('overview'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.benchmarkMetadataCard__overview, domain=None, range=Optional[str])

slots.benchmarkMetadataCard__type = Slot(uri=NEXUS.type, name="benchmarkMetadataCard__type", curie=NEXUS.curie('type'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.benchmarkMetadataCard__type, domain=None, range=Optional[str])

slots.question__text = Slot(uri=NEXUS.text, name="question__text", curie=NEXUS.curie('text'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.question__text, domain=None, range=str)

slots.controlActivity__type = Slot(uri=NEXUS.type, name="controlActivity__type", curie=NEXUS.curie('type'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.controlActivity__type, domain=None, range=Optional[str])

slots.controlActivityPermission__type = Slot(uri=NEXUS.type, name="controlActivityPermission__type", curie=NEXUS.curie('type'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.controlActivityPermission__type, domain=None, range=Optional[str])

slots.controlActivityProhibition__type = Slot(uri=NEXUS.type, name="controlActivityProhibition__type", curie=NEXUS.curie('type'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.controlActivityProhibition__type, domain=None, range=Optional[str])

slots.controlActivityObligation__type = Slot(uri=NEXUS.type, name="controlActivityObligation__type", curie=NEXUS.curie('type'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.controlActivityObligation__type, domain=None, range=Optional[str])

slots.controlActivityRecommendation__type = Slot(uri=NEXUS.type, name="controlActivityRecommendation__type", curie=NEXUS.curie('type'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.controlActivityRecommendation__type, domain=None, range=Optional[str])

slots.requirement__type = Slot(uri=NEXUS.type, name="requirement__type", curie=NEXUS.curie('type'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.requirement__type, domain=None, range=Optional[str])

slots.composed_of = Slot(uri=AI_GOVERNANCE_FRAMEWORK.composed_of, name="composed_of", curie=AI_GOVERNANCE_FRAMEWORK.curie('composed_of'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.composed_of, domain=None, range=Optional[Union[str, QuestionId]])

slots.RiskControlGroup_hasPart = Slot(uri=SKOS.member, name="RiskControlGroup_hasPart", curie=SKOS.curie('member'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.RiskControlGroup_hasPart, domain=RiskControlGroup, range=Optional[Union[Union[str, RiskControlId], list[Union[str, RiskControlId]]]])

slots.RiskGroup_hasPart = Slot(uri=SKOS.member, name="RiskGroup_hasPart", curie=SKOS.curie('member'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.RiskGroup_hasPart, domain=RiskGroup, range=Optional[Union[Union[str, RiskId], list[Union[str, RiskId]]]])

slots.Risk_isPartOf = Slot(uri=SCHEMA.isPartOf, name="Risk_isPartOf", curie=SCHEMA.curie('isPartOf'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.Risk_isPartOf, domain=Risk, range=Optional[Union[str, RiskGroupId]])

slots.CapabilityDomain_hasPart = Slot(uri=SKOS.member, name="CapabilityDomain_hasPart", curie=SKOS.curie('member'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.CapabilityDomain_hasPart, domain=CapabilityDomain, range=Optional[Union[Union[str, CapabilityGroupId], list[Union[str, CapabilityGroupId]]]])

slots.CapabilityGroup_hasPart = Slot(uri=SKOS.member, name="CapabilityGroup_hasPart", curie=SKOS.curie('member'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.CapabilityGroup_hasPart, domain=CapabilityGroup, range=Optional[Union[Union[str, CapabilityId], list[Union[str, CapabilityId]]]])

slots.CapabilityGroup_isPartOf = Slot(uri=SCHEMA.isPartOf, name="CapabilityGroup_isPartOf", curie=SCHEMA.curie('isPartOf'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.CapabilityGroup_isPartOf, domain=CapabilityGroup, range=Optional[Union[str, CapabilityDomainId]])

slots.CapabilityGroup_belongsToDomain = Slot(uri=SCHEMA.isPartOf, name="CapabilityGroup_belongsToDomain", curie=SCHEMA.curie('isPartOf'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.CapabilityGroup_belongsToDomain, domain=CapabilityGroup, range=Optional[Union[str, CapabilityDomainId]])

slots.Capability_isPartOf = Slot(uri=SCHEMA.isPartOf, name="Capability_isPartOf", curie=SCHEMA.curie('isPartOf'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.Capability_isPartOf, domain=Capability, range=Optional[Union[str, CapabilityGroupId]])

slots.Capability_requiredByTask = Slot(uri=NEXUS.requiredByTask, name="Capability_requiredByTask", curie=NEXUS.curie('requiredByTask'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.Capability_requiredByTask, domain=Capability, range=Optional[Union[Union[str, AiTaskId], list[Union[str, AiTaskId]]]])

slots.Capability_implementedByAdapter = Slot(uri=NEXUS.implementedByAdapter, name="Capability_implementedByAdapter", curie=NEXUS.curie('implementedByAdapter'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.Capability_implementedByAdapter, domain=Capability, range=Optional[Union[Union[str, AdapterId], list[Union[str, AdapterId]]]])

slots.AiSystem_isComposedOf = Slot(uri=NEXUS.isComposedOf, name="AiSystem_isComposedOf", curie=NEXUS.curie('isComposedOf'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.AiSystem_isComposedOf, domain=None, range=Optional[Union[Union[str, BaseAiId], list[Union[str, BaseAiId]]]])

slots.AiSystem_hasCapability = Slot(uri=TECH.hasCapability, name="AiSystem_hasCapability", curie=TECH.curie('hasCapability'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.AiSystem_hasCapability, domain=None, range=Optional[Union[Union[str, CapabilityId], list[Union[str, CapabilityId]]]])

slots.AiAgent_isProvidedBy = Slot(uri=AIRO.isProvidedBy, name="AiAgent_isProvidedBy", curie=AIRO.curie('isProvidedBy'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.AiAgent_isProvidedBy, domain=None, range=Optional[Union[str, AiProviderId]])

slots.LargeLanguageModel_isPartOf = Slot(uri=SCHEMA.isPartOf, name="LargeLanguageModel_isPartOf", curie=SCHEMA.curie('isPartOf'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.LargeLanguageModel_isPartOf, domain=None, range=Optional[Union[str, LargeLanguageModelFamilyId]])

slots.AiTask_requiresCapability = Slot(uri=NEXUS.requiresCapability, name="AiTask_requiresCapability", curie=NEXUS.curie('requiresCapability'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.AiTask_requiresCapability, domain=AiTask, range=Optional[Union[Union[str, CapabilityId], list[Union[str, CapabilityId]]]])

slots.AiTaskDomain_hasPart = Slot(uri=SKOS.member, name="AiTaskDomain_hasPart", curie=SKOS.curie('member'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.AiTaskDomain_hasPart, domain=AiTaskDomain, range=Optional[Union[Union[str, AiTaskGroupId], list[Union[str, AiTaskGroupId]]]])

slots.AiTaskGroup_hasPart = Slot(uri=SKOS.member, name="AiTaskGroup_hasPart", curie=SKOS.curie('member'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.AiTaskGroup_hasPart, domain=AiTaskGroup, range=Optional[Union[Union[str, AiTaskId], list[Union[str, AiTaskId]]]])

slots.AiTaskGroup_isPartOf = Slot(uri=SCHEMA.isPartOf, name="AiTaskGroup_isPartOf", curie=SCHEMA.curie('isPartOf'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.AiTaskGroup_isPartOf, domain=AiTaskGroup, range=Optional[Union[str, AiTaskDomainId]])

slots.Stakeholder_isPartOf = Slot(uri=SCHEMA.isPartOf, name="Stakeholder_isPartOf", curie=SCHEMA.curie('isPartOf'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.Stakeholder_isPartOf, domain=Stakeholder, range=Optional[Union[str, StakeholderGroupId]])

slots.AiEval_isComposedOf = Slot(uri=NEXUS.isComposedOf, name="AiEval_isComposedOf", curie=NEXUS.curie('isComposedOf'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.AiEval_isComposedOf, domain=AiEval, range=Optional[Union[Union[str, AiEvalId], list[Union[str, AiEvalId]]]])

slots.Questionnaire_composed_of = Slot(uri=AI_GOVERNANCE_FRAMEWORK.composed_of, name="Questionnaire_composed_of", curie=AI_GOVERNANCE_FRAMEWORK.curie('composed_of'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.Questionnaire_composed_of, domain=Questionnaire, range=Optional[Union[str, QuestionId]])

slots.Adapter_implementsCapability = Slot(uri=NEXUS.implementsCapability, name="Adapter_implementsCapability", curie=NEXUS.curie('implementsCapability'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.Adapter_implementsCapability, domain=Adapter, range=Optional[Union[Union[str, CapabilityId], list[Union[str, CapabilityId]]]])

slots.LLMIntrinsic_implementsCapability = Slot(uri=NEXUS.implementsCapability, name="LLMIntrinsic_implementsCapability", curie=NEXUS.curie('implementsCapability'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.LLMIntrinsic_implementsCapability, domain=LLMIntrinsic, range=Optional[Union[Union[str, CapabilityId], list[Union[str, CapabilityId]]]])

slots.Requirement_hasRule = Slot(uri=DPV.hasRule, name="Requirement_hasRule", curie=DPV.curie('hasRule'),
                   model_uri=AI_GOVERNANCE_FRAMEWORK.Requirement_hasRule, domain=Requirement, range=Optional[Union[Union[str, RuleId], list[Union[str, RuleId]]]])
