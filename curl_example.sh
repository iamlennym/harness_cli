curl --location --request POST 'https://app.harness.io/gateway/pipeline/api/pipeline/execute/devBootstrap?accountIdentifier=6_vVHzo9Qeu9fXvj-AcbCQ&orgIdentifier=SE_Sandbox&projectIdentifier=Len_Sandbox&moduleType=CI' \
--header 'Content-Type: application/yaml' \
--header 'x-api-key: sat.6_vVHzo9Qeu9fXvj-AcbCQ.6822c0c48de73843c655a00f.tybm2wxaYOtgv8dDHlqZ' \
--data-raw 'pipeline:
  identifier: devBootstrap
  variables:
    - name: APPLICATION_NAME
      type: String
      value: bella'
