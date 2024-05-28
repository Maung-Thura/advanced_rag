#!/bin/sh
# mthura2024 advancedrag 05/18/2024

# Mac
# newip=$(ipconfig getifaddr en0)

# Ubuntu
internal_ip=$(hostname -i)
external_ip=$(curl http://checkip.amazonaws.com)

sed "s/ec2_public_ip/${external_ip}/g" index.html > /var/www/html/index.html
sed "s/ec2_public_ip/${external_ip}/g" httpd.conf > /etc/apache2/httpd.conf
sed "s/ec2_private_ip/${internal_ip}/g" httpd.conf > /etc/apache2/httpd.conf

sudo /etc/init.d/apache2 restart

export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
export LANGCHAIN_API_KEY="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"
export LANGCHAIN_PROJECT="advancedrag"

langflow_instances=$(pgrep --count langflow)

if [ $langflow_instances -ge 1 ];
then
    pkill -9 langflow
fi

echo ""
echo "Langflow server is about to start. Copy below URLs:"
echo ""
echo "Langflow server: http://${external_ip}:7860"
echo "Langflow client: http://${external_ip}:80"
echo ""
read -p 'Press any key to start the langflow server: ' user_input

langflow run --host $internal_ip
