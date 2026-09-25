import { computed, ref, watch } from 'vue'

const neutralOptions = { identities: ['合同当事人'], scenarios: ['一般合同'] }

// Contextual fields belong to one contract; preferences belong to the user.
export function useReviewProfile(contractType, catalog) {
  const userIdentity = ref('合同当事人')
  const contractScenario = ref('一般合同')
  const riskAppetite = ref('标准')
  const bargainingPosition = ref('均衡方')
  const jurisdiction = ref('北京')
  const resolvedIdentity = ref('')
  const resolvedScenario = ref('')
  const options = computed(() => catalog.value[contractType.value] || neutralOptions)
  const identityOptions = computed(() => [...new Set([...options.value.identities, resolvedIdentity.value].filter(Boolean))])
  const scenarioOptions = computed(() => [...new Set([...options.value.scenarios, resolvedScenario.value].filter(Boolean))])

  function resetContext() {
    resolvedIdentity.value = ''
    resolvedScenario.value = ''
    userIdentity.value = options.value.identities[0]
    contractScenario.value = options.value.scenarios[0]
  }
  watch([contractType, catalog], resetContext, { immediate: true, flush: 'sync' })

  function buildProfile() {
    return {
      contract_type: contractType.value,
      user_identity: userIdentity.value,
      review_role: userIdentity.value,
      contract_scenario: contractScenario.value,
      risk_appetite: riskAppetite.value,
      bargaining_position: bargainingPosition.value,
      jurisdiction: jurisdiction.value
    }
  }

  function setProfilePreset(preset) {
    const values = { conservative: ['保守', '弱势方'], standard: ['标准', '均衡方'], aggressive: ['激进', '强势方'] }
    const chosen = values[preset] || values.standard
    riskAppetite.value = chosen[0]
    bargainingPosition.value = chosen[1]
  }

  return { userIdentity, contractScenario, riskAppetite, bargainingPosition, jurisdiction,
    identityOptions, scenarioOptions, resetContext, buildProfile, setProfilePreset }
}
