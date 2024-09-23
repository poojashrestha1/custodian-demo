echo "Executing custodian policies in policies/all-accounts-policies/ folder"

  if [ "$(find ./policies/all-accounts-policies/*.yml 2> /dev/null | wc -l )" -gt 0 ]; then
    for file in ./policies/all-accounts-policies/*.yml; do
      echo "Deploying policy $file"
      c7n-org run -c ./configs/all_accounts.yml -s ./all-accounts -u "$file" -v
    done

echo "Executing custodian policies in policies/shared-ou-accounts-policies/ folder"

  if [ "$(find ./policies/shared-ou-accounts-policies/*.yml 2> /dev/null | wc -l )" -gt 0 ]; then
    for file in ./policies/shared-ou-accounts-policies/*.yml; do
      echo "Deploying policy $file"
      c7n-org run -c ./configs/shared_ou_accounts.yml -s ./shared-ou-accounts -u "$file" -v
    done

echo "Executing custodian policies in policies/security-ou-accounts-policies/ folder"

  if [ "$(find ./policies/security-ou-accounts-policies/*.yml 2> /dev/null | wc -l )" -gt 0 ]; then
    for file in ./policies/security-ou-accounts-policies/*.yml; do
      echo "Deploying policy $file"
      c7n-org run -c ./configs/security_ou_accounts.yml -s ./security-ou-accounts -u "$file" -v
    done

echo "Executing custodian policies in policies/development-ou-accounts-policies/ folder"

  if [ "$(find ./policies/development-ou-accounts-policies/*.yml 2> /dev/null | wc -l )" -gt 0 ]; then
    for file in ./policies/development-ou-accounts-policies/*.yml; do
      echo "Deploying policy $file"
      c7n-org run -c ./configs/development_ou_accounts.yml -s ./development-ou-accounts -u "$file" -v
    done

echo "Executing custodian policies in policies/development-ou-accounts-policies/ folder"

  if [ "$(find ./policies/production-ou-accounts-policies/*.yml 2> /dev/null | wc -l )" -gt 0 ]; then
    for file in ./policies/production-ou-accounts-policies/*.yml; do
      echo "Deploying policy $file"
      c7n-org run -c ./configs/production_ou_accounts.yml -s ./production-ou-accounts -u "$file" -v
    done