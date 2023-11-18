local httpservice = game:GetService("HttpService")
game.Players.PlayerAdded:Connect(function(plr)
    
	local success, response = pcall(function()
		return httpservice:GetAsync("yourapiadress/api/robloxwhitelist/discordinfo/" .. tostring(plr.UserId))
	end)

	if success then
		local decodedResponse = httpservice:JSONDecode(response) 
		
		print("Odebrano dane JSON:")
		print(decodedResponse)
		if not decodedResponse["Not found"] then
			if decodedResponse["Verified"] == 1 then
				local DiscordNickValue = decodedResponse["DiscordNick"]
				local DiscordIDValue = decodedResponse["DiscordID"]
				plr:SetAttribute("DiscordNick", DiscordNickValue)
				plr:SetAttribute("DiscordID", DiscordIDValue)
			else
				plr:Kick("Nie masz zweryfikowanego konta Discord do konta Roblox! Zweryfikuj je na Discordzie lub jeśli wystąpił błąd skontaktuj się z administracją bota!")
			end
			
		else
			plr:Kick("Nie znaleziono Cię na liście whitelist bota AurusVerification! Zweryfikuj się na Discordzie lub jeśli wystąpił błąd skontaktuj się z administracją bota!")
		end
		
		
	else
		print("Błąd podczas wykonywania zapytania API:", response)
		plr:Kick("Błąd z połączeniem z zewnętrzną bazą danych bota AurusVerification! Jeśli ponowna próba nie powiedzie się skontaktuj się z administracją bota!")
	end
	
end)
